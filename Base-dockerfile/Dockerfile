# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables
ENV MAVEN_VERSION=3.9.4
ENV SONAR_SCANNER_VERSION=4.8.0.2856
ENV JFROG_CLI_VERSION=2.47.0
ENV TRIVY_VERSION=0.54.1

# Install required packages
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    openjdk-11-jdk \
    git \
    docker.io \
    nodejs \
    npm \
    unzip \
    ca-certificates \
    openssl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Snyk
RUN npm install -g snyk

# Install Sonar Scanner
RUN curl -fsSL https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip -o sonar-scanner.zip \
    && unzip sonar-scanner.zip -d /opt \
    && ln -s /opt/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner \
    && rm sonar-scanner.zip

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Set Java Home (for Sonar Scanner)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH=$JAVA_HOME/bin:$PATH

# Verify installations
RUN sonar-scanner --version && snyk --version && trivy --version

# Set the entrypoint to bash
ENTRYPOINT ["/bin/bash"]