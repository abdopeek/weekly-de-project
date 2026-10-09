import logging
from init_db import initialize_schema
from load_data import load_all_datasets
from verify_db import verify_counts
from analytics import run_analytics

logger = logging.getLogger("Pipeline_Orchestrator")


def run_pipeline(reset_first: bool = False):
    logger.info("Starting end-to-end data pipeline execution...")

    try:
        if reset_first:
            logger.info("Step 1: Initializing fresh schema...")
            initialize_schema()

        logger.info("Step 2: Running idempotent data loading...")
        load_all_datasets()

        logger.info("Step 3: Verifying table counts...")
        verify_counts()

        logger.info("Step 4: Executing analytical queries...")
        run_analytics()

        logger.info("Pipeline execution finished successfully!")

    except Exception as e:
        logger.error(f"Pipeline crashed during execution: {e}", exc_info=True)


if __name__ == "__main__":
    run_pipeline(reset_first=False)