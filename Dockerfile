# Use official Python image
FROM python:3.11.11

# Create a non-root user
RUN useradd -m -u 1000 user

# Set environment variables
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory
WORKDIR $HOME/app

# Copy only necessary files first (for better Docker caching)
COPY --chown=user requirements.txt pyproject.toml ./

# Install dependencies using UV (since you are using UV)
RUN pip install uv && uv pip install -r requirements.txt

# Copy the rest of the application files
COPY --chown=user . .

# Expose the port (optional, but good practice)
EXPOSE 7860

# Run Chainlit app
CMD ["chainlit", "run", "app.py", "--port", "7860"]
