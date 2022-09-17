# ============================================================
# variables
# ============================================================
variable "project_id" {
  # change it for yours
  # default = "YOUR_PROJECT_ID"
  default = "soa-projects"
}

variable "region" {
  # change it for yours
  default = "us-central1"
}

# ============================================================
# provider: Google Cloud platform
# ============================================================

# main terraform configuration
provider "google" {
  project = var.project_id
  region  = var.region
}

# ============================================================
# resource: bucket
# ============================================================

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

# Creates a new bucket in Google Cloud Storage Service (GCS).
# Once a bucket has been created, its location can't be changed.
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-function_bucket"
  location = var.region
  force_destroy = true
}

resource "google_storage_bucket" "images" {
  name          = "${var.project_id}-images"
  location      = var.region
  force_destroy = true
}

# ============================================================
# resource: code
# ============================================================

data "archive_file" "source" {
  type        = "zip"
  source_dir  = "code"
  output_path = "/tmp/cloud_function.zip"
}

# ============================================================
# bucket
# ============================================================

resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"

  # Append to the MD5 checksum of the files's content
  # to force the zip to be updated as soon as a change occurs
  name   = "src-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name

  # Dependencies are automatically inferred so these lines can be deleted
  depends_on = [
    google_storage_bucket.function_bucket, # declared in `storage.tf`
    data.archive_file.source
  ]
}

# ============================================================
# log
# ============================================================

# backend who reads the states
terraform {
  backend "local" {
  }
}

# ============================================================
# function
# ============================================================

# Create the Cloud function triggered by a `Finalize` event on the bucket
resource "google_cloudfunctions_function" "function" {
  name    = "myFunction"
  runtime = "python37" # of course changeable

  # Get the source code of the cloud function as a Zip compression
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  # Must match the function name in the cloud function `main.py` source code
  entry_point = "main"

  # execute this function when there is a change in bucket 
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = "${var.project_id}-images"
  }

  # Dependencies are automatically inferred so these lines can be deleted
  depends_on = [
    google_storage_bucket_object.zip,
    google_storage_bucket.function_bucket,
    google_storage_bucket.images
  ]
}
