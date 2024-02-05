import logging


def get_debug_logger(log_file_path="debug.log"):

    logging.basicConfig(
        filename="debug.log",
        level=logging.DEBUG,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    # Create a logger
    logger = logging.getLogger("debug")

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Create a file handler and set the formatter
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # # Remove existing handlers
    # for existing_handler in logger.handlers:
    #     logger.removeHandler(existing_handler)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def post_process_ner(raw_entities, islist=False):
    processed_entites = []
    if islist:
        for entity_list in raw_entities:
            processed_entity_list = []
            for entities in entity_list:
                processed_entites.append(
                    {
                        "entity": entities["entity_group"],
                        "work": entities["word"],
                        "entity_start": int(entities["start"]),
                        "entity_end": int(entities["end"]),
                    }
                )
            if processed_entity_list:
                processed_entites.append(processed_entity_list)
    else:
        for entities in raw_entities:
            processed_entites.append(
                {
                    "entity": entities["entity_group"],
                    "work": entities["word"],
                    "entity_start": int(entities["start"]),
                    "entity_end": int(entities["end"]),
                }
            )

    return processed_entites
