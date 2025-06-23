Recommended Approach: Integrate Model Creation Inside the Container
Given your statement that “it is very likely that the model will change,” the integrate model creation inside the container approach is the best practice. This approach aligns with modern CI/CD principles, ensures reproducibility, keeps the Git repository lightweight, and automates the entire process. Here’s why:
Frequent Model Changes: Committing a new my_keras.model file to Git for every change will quickly bloat the repository and make version control cumbersome. Building the model in the container avoids this.

Reproducibility: By generating the model in the same environment as the runtime, you eliminate risks of environment mismatches (e.g., TensorFlow version differences).

Automation: Integrating model creation into the Docker build and GitHub Actions pipeline streamlines the workflow, reducing manual intervention.

Scalability: This approach is maintainable for frequent updates to the model-building script or training logic.

To address the main drawback (slower Docker builds), you can optimize the build process using Docker layer caching and ensure GitHub Actions runners have sufficient resources. If build times become prohibitive, you can explore hybrid approaches (e.g., caching the model in a registry), but the fully integrated approach is simpler for now.

my_project/
├── Dockerfile
├── .github/
│   └── workflows/
│       └── build-docker.yml
├── scripts/
│   └── train_model.py
├── requirements.txt
├── README.md
└── .gitignore
