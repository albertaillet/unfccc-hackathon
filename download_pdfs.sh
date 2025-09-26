#!/bin/bash

# UNFCCC PDF Downloader - Automated Workflow Script
# This script collects Access document links if they don't exist, then downloads PDFs

set -e  # Exit on any error

# Default values
LINKS_FILE="${1:-access_document_links.txt}"
DOWNLOAD_DIR="${2:-downloads}"

# Function to print output
print_status() {
    echo "[INFO] $1"
}

print_success() {
    echo "[SUCCESS] $1"
}

print_warning() {
    echo "[WARNING] $1"
}

print_error() {
    echo "[ERROR] $1"
}

# Function to check if uv is installed
check_uv() {
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Please install uv first."
        print_status "Visit: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
}

# Function to check if links file exists and has content
check_links_file() {
    if [[ -f "$LINKS_FILE" && -s "$LINKS_FILE" ]]; then
        local line_count=$(wc -l < "$LINKS_FILE")
        print_success "Links file '$LINKS_FILE' exists with $line_count URLs"
        return 0
    else
        print_warning "Links file '$LINKS_FILE' does not exist or is empty"
        return 1
    fi
}

# Function to collect links
collect_links() {
    print_status "Collecting Access document links..."
    if uv run python link_collector.py "$LINKS_FILE"; then
        if check_links_file; then
            print_success "Link collection completed successfully"
            return 0
        else
            print_error "Link collection failed - no URLs found"
            return 1
        fi
    else
        print_error "Link collection failed"
        return 1
    fi
}

# Function to download PDFs
download_pdfs() {
    print_status "Starting PDF download process..."
    print_status "Links file: $LINKS_FILE"
    print_status "Download directory: $DOWNLOAD_DIR"
    
    if uv run python pdf_downloader.py "$LINKS_FILE" "$DOWNLOAD_DIR"; then
        print_success "PDF download process completed"
        
        # Count downloaded files
        if [[ -d "$DOWNLOAD_DIR" ]]; then
            local pdf_count=$(find "$DOWNLOAD_DIR" -name "*.pdf" | wc -l)
            print_success "Downloaded $pdf_count PDF files to '$DOWNLOAD_DIR'"
        fi
        return 0
    else
        print_error "PDF download process failed"
        return 1
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "UNFCCC PDF Downloader - Automated Workflow"
    echo "=========================================="
    echo
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    check_uv
    
    # Check if links file exists
    if ! check_links_file; then
        print_status "Collecting links first..."
        if ! collect_links; then
            print_error "Failed to collect links. Exiting."
            exit 1
        fi
    else
        print_status "Using existing links file: $LINKS_FILE"
    fi
    
    echo
    
    # Download PDFs
    if download_pdfs; then
        echo
        print_success "Workflow completed successfully!"
        print_status "Check the '$DOWNLOAD_DIR' directory for downloaded PDFs"
    else
        print_error "Workflow failed during PDF download"
        exit 1
    fi
}

# Show usage if help requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [links_file] [download_directory]"
    echo
    echo "Arguments:"
    echo "  links_file        File to store/read Access document links (default: access_document_links.txt)"
    echo "  download_directory Directory to save downloaded PDFs (default: downloads)"
    echo
    echo "Examples:"
    echo "  $0                                    # Use defaults"
    echo "  $0 my_links.txt                      # Custom links file"
    echo "  $0 my_links.txt my_downloads         # Custom links file and download directory"
    echo
    echo "This script will:"
    echo "  1. Check if links file exists and has content"
    echo "  2. If not, collect Access document links from UNFCCC COP-29 page"
    echo "  3. Download English PDFs from all collected links"
    exit 0
fi

# Run main function
main "$@"