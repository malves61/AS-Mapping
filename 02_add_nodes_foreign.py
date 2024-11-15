def add_info_nodes(main_path, maxseqerr = 3):
    """queries and sabes description form bgpview.io API.
           In case of failure or interruption, just run again to continue.

        Parameters
        ----------
        main_path : pahtlib:Path, mandatory
            Root directory for ASN analysis data.
        maxseqerr : int
            Max sequential errors before interrupting/aborting

        Returns
        ------
        0
            Always.
    """
    nodes_path=Path(main_path,'json','br')
    f_nodes_path=Path(main_path, 'json','foreign')
    uppeers_path=Path(main_path,'json','uppeers')

    # get exist file list from the br, foreign and up peers nodes directories.
    nodes_list = [x.stem for x in list(nodes_path.glob('*.json'))]
    fnodes_list = [x.stem for x in list(f_nodes_path.glob('*.json'))]
    uppeers_list = [x.stem for x in list(uppeers_path.glob('*.json'))]

    logging.info(f'There are {len(nodes_list)} br nodes (folder {str(nodes_path)}), {len(fnodes_list)} foreign folders on folder {str(f_nodes_path)} and {len(uppeers_list)} peers on folder {str(uppeers_path)}.')
    print(f'There are {len(nodes_list)} br nodes (folder {str(nodes_path)}), {len(fnodes_list)} foreign folders on folder {str(f_nodes_path)} and {len(uppeers_list)} peers on folder {str(uppeers_path)}.')

    existing_nodes_list = list(set(nodes_list+fnodes_list))
    logging.info(f'There are a total of {len(existing_nodes_list)} nodes.')
    print(f'There are a total of {len(existing_nodes_list)} nodes.')
    add_nodes = []

    # builds add_nodes list for existing nodes on up peers directory that have no description yet
    for file in list(uppeers_path.glob('*.json')):
        if file.stem not in existing_nodes_list:
            json_Content=json.loads(file.read_text(encoding="UTF-8"))
            if json_Content['status']=='ok':
                add_nodes.append(str(file.stem))
                for peer in json_Content['data']['ipv4_upstreams']:
                    if str(peer['asn']) not in existing_nodes_list:
                        add_nodes.append(str(peer['asn']))
                for peer in json_Content['data']['ipv6_upstreams']:
                    if str(peer['asn']) not in existing_nodes_list:
                        add_nodes.append(str(peer['asn']))
    add_nodes = list(set(add_nodes))
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    count = 0
    total = len(add_nodes)
    logging.info(f'There are {total} nodes to describe.')
    print(f'There are {total} nodes to describe.')
    subsequent_errors = 0
    no_info = 0

    # queries for node information not yet obtained.
    for node in add_nodes:
        url = 'https://api.bgpview.io/asn/'+str(node)
        try:
            resp = requests.get(url, headers = headers)
            resp.raise_for_status()
            # access JSOn content to check if data was received
            jsonResponse = resp.json()
            if jsonResponse['status']=='ok':
                subsequent_errors = 0
                if jsonResponse['data']['country_code']=='BR':
                    with open(str(nodes_path)+'/'+node+'.json', 'w') as outfile:
                        json.dump(jsonResponse, outfile)
                    print(f'AS{node} - {count}/{total} - OK - on BR')
                elif jsonResponse['data']['country_code']=='':
                    with open(str(nodes_path)+'/'+node+'.json', 'w') as outfile:
                        json.dump(jsonResponse, outfile)
                    print(f'AS{node} - {count}/{total} - no country_code information')
                    no_info=no_info+1
                else:
                    with open(str(f_nodes_path)+'/'+node+'.json', 'w') as outfile:
                        json.dump(jsonResponse, outfile)
                    print(f'AS{node} - {count}/{total} - OK - Foreign')
        except:
            logging.error(f'Error on quering AS{node} information.')
            print(node,'Error on quering AS{node} information.)
            subsequent_errors = subsequent_errors+1
            if subsequent_errors > maxseqerr:
                logging.critical('Too many sequential errors. Aborting.')
                raise Exception('Too many sequential errors. Aborting.')
        count=count+1
        sleep(0.1)
    logging.info(f'There are no country_code information for {no_info} nodes.')
    print(f'There are no country_code information for {no_info} nodes.')

    return 0

if __name__ == "__main__":
    import json
    import logging
    import pandas as pd
    from pathlib import Path
    import requests
    from time import sleep


    main_path=Path('/content/drive/MyDrive/Anatel /ASN2')
    log_file = Path(main_path,'ASN_check.log')
    logging.basicConfig(filename=str(log_file), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

    add_info_nodes(main_path)
