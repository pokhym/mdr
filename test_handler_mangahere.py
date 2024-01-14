import logging

if __name__ == "__main__":
  # Setup Logging
  logging.basicConfig(level=logging.INFO
                      , format="%(asctime)s;%(levelname)s;%(message)s"
                      , datefmt="%Y-%m-%d %H:%M:%S"
                      , filename="test_log.txt"
                      , filemode="w")
  # define a Handler which writes INFO messages or higher to the sys.stderr
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  # set a format which is simpler for console use
  formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
  # tell the handler to use this format
  console.setFormatter(formatter)
  # add the handler to the root logger
  logging.getLogger().addHandler(console)