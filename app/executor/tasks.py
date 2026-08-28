from app.extensions import celery_app, db
from app.pipelines.models import Pipeline, PipelineExecution
import time
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def execute_pipeline_task(self, execution_id):
    """
    Celery task to run a pipeline asynchronously.
    """
    # Requires app context for DB access if running in a separate worker
    # In a real setup, Celery needs Flask app context pushed here.
    logger.info(f"Starting pipeline execution: {execution_id}")
    try:
        # Simulate execution logic
        time.sleep(2)
        logger.info(f"Pipeline {execution_id} completed successfully.")
        return {"status": "success", "execution_id": execution_id}
    except Exception as exc:
        logger.error(f"Pipeline execution failed: {exc}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
