# Research: Deploy Django to Google Cloud

**Decision**: Use Google App Engine for deployment.

**Rationale**: Google App Engine is a fully managed, serverless platform that is well-suited for Django applications. It handles scaling, load balancing, and versioning automatically, which aligns with the project's goal of a simple and maintainable deployment process. The existing `python27` project was also an App Engine project, so this maintains consistency.

**Alternatives Considered**:
- **Google Compute Engine**: This would provide more control over the environment but would also require more manual configuration and management.
- **Google Kubernetes Engine**: This is a powerful option for containerized applications but adds significant complexity that is not necessary for this project at this stage.

**Key Findings**:
- An `app.yaml` file is required to configure the App Engine service.
- The `gcloud app deploy` command is used to deploy the application.
- Static files can be served by App Engine.
- Database migrations need to be run as part of the deployment process.
