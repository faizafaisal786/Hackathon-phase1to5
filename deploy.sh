#!/bin/bash

# 🚀 One-Click Deployment Script for All Phases
# Professional Hackathon Todo Project

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "=================================="
echo "  HACKATHON TODO - DEPLOYMENT"
echo "=================================="
echo -e "${NC}"

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."

    if ! command -v git &> /dev/null; then
        print_error "Git is not installed"
        exit 1
    fi
    print_success "Git installed"

    if ! command -v python &> /dev/null; then
        print_error "Python is not installed"
        exit 1
    fi
    print_success "Python installed"

    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi
    print_success "Node.js installed"

    if ! command -v docker &> /dev/null; then
        print_info "Docker not installed (optional for Phase 4)"
    else
        print_success "Docker installed"
    fi

    if ! command -v vercel &> /dev/null; then
        print_info "Vercel CLI not installed. Installing..."
        npm install -g vercel
        print_success "Vercel CLI installed"
    else
        print_success "Vercel CLI installed"
    fi
}

# Phase 1 Deployment
deploy_phase1() {
    echo ""
    echo -e "${BLUE}=== Phase 1: CLI to Web ===${NC}"

    print_info "Deploying to Vercel..."
    cd todo-phase1

    # Create vercel config if not exists
    if [ ! -f "vercel.json" ]; then
        print_error "vercel.json not found"
        exit 1
    fi

    print_success "Configuration found"

    # Deploy
    print_info "Starting deployment..."
    vercel --prod --yes

    cd ..
    print_success "Phase 1 deployed!"
}

# Phase 2 Backend Deployment
deploy_phase2_backend() {
    echo ""
    echo -e "${BLUE}=== Phase 2: Backend ===${NC}"

    cd hackathon-todo

    print_info "Installing dependencies..."
    pip install -r requirements.txt

    print_info "Testing backend..."
    python test_app.py

    if [ $? -eq 0 ]; then
        print_success "All tests passed!"
    else
        print_error "Tests failed!"
        exit 1
    fi

    print_info "Backend ready for deployment"
    print_info "Deploy to Railway or Render manually"
    print_info "Command: railway up OR render deploy"

    cd ..
}

# Phase 2 Frontend Deployment
deploy_phase2_frontend() {
    echo ""
    echo -e "${BLUE}=== Phase 2: Frontend ===${NC}"

    cd hackathon-todo/frontend

    print_info "Installing dependencies..."
    npm install

    print_info "Building frontend..."
    npm run build

    if [ $? -eq 0 ]; then
        print_success "Build successful!"
    else
        print_error "Build failed!"
        exit 1
    fi

    print_info "Deploying to Vercel..."
    vercel --prod --yes

    cd ../..
    print_success "Phase 2 Frontend deployed!"
}

# Phase 4 Docker
deploy_phase4() {
    echo ""
    echo -e "${BLUE}=== Phase 4: Docker ===${NC}"

    cd hackathon-todo

    if ! command -v docker &> /dev/null; then
        print_error "Docker not installed. Skipping Phase 4."
        cd ..
        return
    fi

    print_info "Building Docker images..."

    docker build -f Dockerfile.backend-simple -t hackathon-todo-backend:latest .
    print_success "Backend image built"

    docker build -f Dockerfile.frontend-simple -t hackathon-todo-frontend:latest .
    print_success "Frontend image built"

    print_info "Starting containers..."
    docker-compose up -d

    print_success "Phase 4 Docker containers running!"
    print_info "Backend: http://localhost:8000"
    print_info "Frontend: http://localhost:3000"

    cd ..
}

# Main menu
show_menu() {
    echo ""
    echo -e "${YELLOW}Select deployment option:${NC}"
    echo "1. Deploy Phase 1 (CLI to Web)"
    echo "2. Deploy Phase 2 Backend"
    echo "3. Deploy Phase 2 Frontend"
    echo "4. Deploy Phase 4 (Docker)"
    echo "5. Deploy All Phases"
    echo "6. Check Prerequisites Only"
    echo "7. Exit"
    echo ""
    read -p "Enter choice [1-7]: " choice
}

# Main script
main() {
    check_prerequisites

    if [ "$1" == "all" ]; then
        deploy_phase1
        deploy_phase2_backend
        deploy_phase2_frontend
        deploy_phase4
    else
        show_menu

        case $choice in
            1)
                deploy_phase1
                ;;
            2)
                deploy_phase2_backend
                ;;
            3)
                deploy_phase2_frontend
                ;;
            4)
                deploy_phase4
                ;;
            5)
                deploy_phase1
                deploy_phase2_backend
                deploy_phase2_frontend
                deploy_phase4
                ;;
            6)
                print_success "Prerequisites check complete!"
                ;;
            7)
                print_info "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid choice"
                exit 1
                ;;
        esac
    fi

    echo ""
    echo -e "${GREEN}=================================="
    echo "  DEPLOYMENT COMPLETE!"
    echo "==================================${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Check your deployments"
    echo "2. Update README with live URLs"
    echo "3. Create demo videos"
    echo "4. Share with hackathon judges"
    echo ""
}

# Run main
main "$@"
