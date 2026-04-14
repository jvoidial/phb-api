#!/bin/bash

# Touch a file to break Docker cache
echo "# force rebuild $(date)" >> Dockerfile

echo "Dockerfile updated to force rebuild."
