SET NLTK_DATA_PATH=C:\Users\appveyor\AppData\Roaming\nltk_data

IF EXIST %NLTK_DATA_PATH% GOTO NLTK_EXISTS
  python -m nltk.downloader punkt
  python -m nltk.downloader maxent_treebank_pos_tagger
  python -m nltk.downloader averaged_perceptron_tagger
  GOTO NLTK_ENDIF
:NLTK_EXISTS
  echo Using cached NLTK data from %NLTK_DATA_PATH%.
:NLTK_ENDIF
