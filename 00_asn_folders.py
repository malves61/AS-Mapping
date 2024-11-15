def validate_path(main_path):
    """Validate path (directories) for ASN data analysis.

        Parameters
        ----------
        main_path : Type Path from pathlib library, mandatory
            Root directory for ASN data analysis.

        Raises
        ------
        Exception
            If main_path parameter is not valide path:pathlib.
        """
    if not (isinstance(main_path, Path) and main_path.is_dir()):
        logging.critical(f'The directory parameter {main_path} is not valid')
        raise Exception(f'The directory parameter {main_path} is not valid')
    logging.info(f'Directory {str(main_path)} is available.')
    print(f'Directory {str(main_path)} is available.')
    return 0


def make_folder_tree(main_path):
    """Build the directory tree from main_path if it is not present.

       main_path
                |-- json
                        | -- br (nodes in br ASN list)
                        | -- foreign (nodes not in br ASN list)
                        | -- uppeers (ASN Up Peers)

        Parameters
        ----------
        main_path : Type Path from pathlib library, mandatory
            Root directory for ASN data analysis.

        Return
        ------
        0
           In any condition.
        """
    Path(main_path,'json','br').mkdir(parents=True, exist_ok=True)
    Path(main_path,'json','foreign').mkdir(parents=True, exist_ok=True)
    Path(main_path,'json','uppeers').mkdir(parents=True, exist_ok=True)
    logging.info(f'Directory tree OK.')
    print(f'Directory tree OK.')
    return 0


if __name__ == "__main__":
    import logging
    import networkx as nx
    import pandas as pd
    from pathlib import Path


    main_path=Path('/content/drive/MyDrive/Anatel /ASN2')
    log_file = Path(main_path,'ASN_check.log')
    logging.basicConfig(filename=str(log_file), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

    validate_path(main_path)
    make_folder_tree(main_path)
