{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPq889y8vT5Qhy8FCeP7MQC",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/malves61/AS-Mapping/blob/master/00_asn_folders.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Versão 18/04/2023"
      ],
      "metadata": {
        "id": "IJkvriMu8HtQ"
      }
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "571ptPkK1D7J",
        "outputId": "7ba69660-fc4d-4946-8743-360d26ca909a"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Mounted at /content/drive\n"
          ]
        }
      ],
      "source": [
        "from google.colab import drive, runtime\n",
        "drive.mount('/content/drive')"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def validate_path(main_path):\n",
        "    \"\"\"Validate path (directories) for ASN data analysis.\n",
        "\n",
        "        Parameters\n",
        "        ----------\n",
        "        main_path : Type Path from pathlib library, mandatory\n",
        "            Root directory for ASN data analysis.\n",
        "\n",
        "        Raises\n",
        "        ------\n",
        "        Exception\n",
        "            If main_path parameter is not valide path:pathlib.\n",
        "        \"\"\"\n",
        "    if not (isinstance(main_path, Path) and main_path.is_dir()):\n",
        "        logging.critical(f'The directory parameter {main_path} is not valid')\n",
        "        raise Exception(f'The directory parameter {main_path} is not valid')\n",
        "    logging.info(f'Directory {str(main_path)} is available.')\n",
        "    print(f'Directory {str(main_path)} is available.')\n",
        "    return 0\n",
        "\n",
        "\n",
        "def make_folder_tree(main_path):\n",
        "    \"\"\"Build the directory tree from main_path if it is not present.\n",
        "\n",
        "       main_path\n",
        "                |-- json\n",
        "                        | -- br (nodes in br ASN list)\n",
        "                        | -- foreign (nodes not in br ASN list)\n",
        "                        | -- uppeers (ASN Up Peers)\n",
        "\n",
        "        Parameters\n",
        "        ----------\n",
        "        main_path : Type Path from pathlib library, mandatory\n",
        "            Root directory for ASN data analysis.\n",
        "\n",
        "        Return\n",
        "        ------\n",
        "        0\n",
        "           In any condition.\n",
        "        \"\"\"\n",
        "    Path(main_path,'json','br').mkdir(parents=True, exist_ok=True)\n",
        "    Path(main_path,'json','foreign').mkdir(parents=True, exist_ok=True)\n",
        "    Path(main_path,'json','uppeers').mkdir(parents=True, exist_ok=True)\n",
        "    logging.info(f'Directory tree OK.')\n",
        "    print(f'Directory tree OK.')\n",
        "    return 0\n",
        "\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    import logging\n",
        "    import networkx as nx\n",
        "    import pandas as pd\n",
        "    from pathlib import Path\n",
        "\n",
        "\n",
        "    main_path=Path('/content/drive/MyDrive/Anatel /ASN2')\n",
        "    log_file = Path(main_path,'ASN_check.log')\n",
        "    logging.basicConfig(filename=str(log_file), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')\n",
        "\n",
        "    validate_path(main_path)\n",
        "    make_folder_tree(main_path)"
      ],
      "metadata": {
        "id": "2uqIiapdkwKr",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "c05e19e3-a660-4602-83cb-1b0395ea715d"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "O diretorio /content/drive/MyDrive/Anatel /ASN2 está presente.\n",
            "Árvore de diretórios OK.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [],
      "metadata": {
        "id": "d2TUMokSmuUj"
      }
    }
  ]
}