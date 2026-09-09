import logging

def setup_logger(verbose: bool = False) -> logging.Logger:
    """
    Configure and return a logger for the GitHub CLI application.

    Args:
        verbose (bool): If True, set the logging level to DEBUG. Otherwise, set it to INFO.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("github_cli")

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO | logging.WARNING)

    formatter = logging.Formatter("[%(levelname)s] %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    #test du logger en mode standard
    log_normal = setup_logger(verbose=False)
    log_normal.warning("Alerte standard (doit s'afficher)")
    log_normal.debug("Detail technique (Ne doit PAS s'afficher)")

    print("-" * 30)

    #test du logger en mode verbose
    log_normal = setup_logger(verbose=True)
    log_normal.info("Message d'information (doit s'afficher)")
    log_normal.debug("Detail technique (doit s'afficher cette fois ci)")