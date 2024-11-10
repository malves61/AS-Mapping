def get_ASN_registrobr(main_path):
    """Downloads ASN list from registro br.

        Parameters
        ----------
        main_path : pathlib:Path, madatory
            Root directory for ASN data analysis.

        Returns
        ------
        0
            Always.
    """
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    registro_br_file=Path(main_path,'nic-asn-blk-latest.txt')

    response = re.get('https://ftp.registro.br/pub/numeracao/origin/nicbr-asn-blk-latest.txt', headers=headers)
    open(registro_br_file, "wb").write(response.content)
    logging.info(f'File {registro_br_file.stem} downloaded.')
    print(f'File {registro_br_file.stem} downloaded.')

    return 0

def get_uppers(main_path, maxseqerr = 3):
    """Reads ASN list file. Checks which up peers should stil be obtained. Queries bgpview.io APN to obtain ASN Uppeers and saves them as json files.
       If it fails (blocked by too many queries) or is interrupted, just run it again to continue from where it stopped.

        Parameters
        ----------
        main_path : pathlib:Path, madatory
            Root directory for ASN data analysis.
        maxseqerr : int
            Max number of sequential errors before interrupting the ASN UP Peer queries.


        Returns
        ------
        0
            Always.
    """
    # define browser headers so bgpview.io do not block queries
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    registro_br_file=Path(main_path,'nic-asn-blk-latest.txt')
    nodes_path=Path(main_path,'json','br')
    uppeers_path=Path(main_path,'json','uppeers')

    registro_br_file=Path(main_path,'nic-asn-blk-latest.txt')
    # reads records from ASN list file (using sep '$') because IP Prefixes are separeted by "|" in the file
    in_registrobr_df=pd.read_csv(registro_br_file,sep='$',header=None)
    # gets the first column up to the first pipe "|"
    registrobr_se = in_registrobr_df[0].str.split('|', n = 1)
    # get first column from ASN list file
    registrobr_alist=registrobr_se.str[0].values.tolist()
    # get nodes that already exist on the corresponding folder.
    nodesbr_list = [x.stem for x in nodes_path.glob('*.json')]
    # builds list with ASN from the ASN list file plus existing nodes on the br nodes folder.
    asn_list= list(set([asn[2:] for asn in registrobr_alist] + nodesbr_list))
    # builds list with AS that have already collected UP Peers on the corresponding folder.
    uppeers_list = [x.stem for x in list(uppeers_path.glob('*.json'))]

    count = len(uppeers_list)
    total = len(asn_list)
    subsequent_errors = 0
    # loop to capture up peers on the asn list but not yet saved on the up peers directory
    for asn in asn_list:
        if not asn in uppeers_list:
            url = 'https://api.bgpview.io/asn/'+str(asn)+'/upstreams'
            try:
                resp = re.get(url, headers = headers)
                resp.raise_for_status()
                # access JSOn content to check if data was received
                jsonResponse = resp.json()
                if jsonResponse['status']=='ok':
                    with open(str(uppeers_path)+'/'+asn+'.json', 'w') as outfile:
                        json.dump(jsonResponse, outfile)
                    subsequent_errors = 0
            except:
#                logging.error(f'Error while acquiring AS upstremas for AS{asn}.')
                print(f'Error while acquiring AS upstreams for AS{asn}.')
                subsequent_errors = subsequent_errors+1
                if subsequent_errors > maxseqerr:
                    logging.critical('Too many sequential errors. Aborting.')
                    raise Exception('Too many sequential errors. Aborting.')
            sleep(0.1)
            count=count+1
            logging.info(f'AS{asn} - {count}/{total}')
            print(f'AS{asn} - {count}/{total}')
    logging.info(f'End of AS Up peers queries')
    print(f'End of AS Up peers queries')

    return 0

if __name__ == "__main__":
    import json
    import logging
    import pandas as pd
    from pathlib import Path
    import requests as re
    from time import sleep

    main_path=Path('/content/drive/MyDrive/Anatel /ASN2')
    log_file = Path(main_path,'ASN_check.log')
    logging.basicConfig(filename=str(log_file), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

    get_ASN_registrobr(main_path)
    get_uppers(main_path, maxseqerr = 5)
