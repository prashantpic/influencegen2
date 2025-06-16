/** @odoo-module */

import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class FileUploaderComponent extends Component {
    setup() {
        // No direct RPC from here; relies on native form submission or parent component handling.
        // If this component were to upload directly via AJAX, it would need rpc/notification services.
        this.notification = useService("notification"); // For client-side validation messages

        this.state = useState({
            selectedFiles: [], // [{ file: File, name: string, size: number, type: string, previewUrl?: string, error?: string }]
            isDragging: false,
        });

        this.fileInputRef = useRef("fileInput");
        this.dropAreaRef = useRef("dropArea");

        // Bind event listeners for drag/drop if dropAreaRef is used
        onMounted(() => {
            if (this.dropAreaRef.el) {
                this.dropAreaRef.el.addEventListener('dragover', this._onDragOver.bind(this), false);
                this.dropAreaRef.el.addEventListener('dragleave', this._onDragLeave.bind(this), false);
                this.dropAreaRef.el.addEventListener('drop', this._onDrop.bind(this), false);
            }
        });
        onWillUnmount(() => {
            if (this.dropAreaRef.el) {
                this.dropAreaRef.el.removeEventListener('dragover', this._onDragOver);
                this.dropAreaRef.el.removeEventListener('dragleave', this._onDragLeave);
                this.dropAreaRef.el.removeEventListener('drop', this._onDrop);
            }
        });
    }

    /**
     * Handle file selection via input or drop.
     * @param {FileList} fileList
     */
    _handleFileSelection(fileList) {
        const filesToAdd = [];
        for (let i = 0; i < fileList.length; i++) {
            const file = fileList[i];
            const validationError = this._validateFile(file);

            if (validationError) {
                 this.notification.add(validationError, { type: 'warning' });
                 // Optionally add to list with error for display, but prevent actual form submission use
                 // filesToAdd.push({ file, name: file.name, size: file.size, type: file.type, error: validationError });
            } else {
                 const fileObject = { file, name: file.name, size: file.size, type: file.type, error: null };
                 // Generate preview for images
                 if (file.type.startsWith('image/')) {
                     fileObject.previewUrl = URL.createObjectURL(file);
                 }
                 filesToAdd.push(fileObject);
            }
        }

        if (this.props.multiple) {
             this.state.selectedFiles = [...this.state.selectedFiles, ...filesToAdd];
        } else {
             // Revoke previous preview URL if any
             if (this.state.selectedFiles.length > 0 && this.state.selectedFiles[0].previewUrl) {
                URL.revokeObjectURL(this.state.selectedFiles[0].previewUrl);
             }
             this.state.selectedFiles = filesToAdd.slice(0, 1);
        }
        this.trigger('files-selected', { files: this.state.selectedFiles.map(f => f.file) });
    }

    /**
     * Client-side file validation (type, size).
     * @param {File} file
     * @returns {string|null} - Error message or null if valid.
     */
    _validateFile(file) {
        if (this.props.acceptedFileTypes) {
            const allowedTypes = this.props.acceptedFileTypes.split(',').map(t => t.trim().toLowerCase());
            const fileType = file.type.toLowerCase();
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

            const typeMatch = allowedTypes.some(allowed => {
                 if (allowed.startsWith('.')) { // Extension match
                      return fileExtension === allowed;
                 } else if (allowed.endsWith('/*')) { // MIME type wildcard match (e.g., image/*)
                      return fileType.startsWith(allowed.slice(0, -1));
                 } else { // Exact MIME type match
                      return fileType === allowed;
                 }
            });

            if (!typeMatch) {
                 return _t("File type '%(fileType)s' for file '%(fileName)s' is not allowed. Accepted types: %(acceptedTypes)s").replace('%(fileType)s', file.type).replace('%(fileName)s', file.name).replace('%(acceptedTypes)s', this.props.acceptedFileTypes);
            }
        }

        if (this.props.maxFileSize && file.size > this.props.maxFileSize) {
            const maxMb = (this.props.maxFileSize / (1024 * 1024)).toFixed(2);
            return _t("File '%(fileName)s' (%(fileSize)sMB) exceeds the maximum allowed size (%(maxSize)sMB).").replace('%(fileName)s', file.name).replace('%(fileSize)s', (file.size / (1024 * 1024)).toFixed(2)).replace('%(maxSize)s', maxMb);
        }
        return null; // Valid
    }


    /**
     * Remove a file from the selected list.
     * @param {Object} fileObject - Object from state.selectedFiles.
     */
    removeFile(fileObject) {
        if (fileObject.previewUrl) {
            URL.revokeObjectURL(fileObject.previewUrl); // Clean up preview object URL
        }
        this.state.selectedFiles = this.state.selectedFiles.filter(f => f !== fileObject);
        this.trigger('files-selected', { files: this.state.selectedFiles.map(f => f.file) });

        // If the component itself holds the input files for direct form submission,
        // we need to update the DataTransfer object of the hidden input. This is tricky.
        // A common pattern is to have the parent component manage the list of files to be uploaded.
        // For simplicity, this component just manages the visual list and validation.
        // The parent form's <input type="file"> still holds the actual files for submission.
        // To clear the input:
        if (this.fileInputRef.el) {
            this.fileInputRef.el.value = ""; // This clears the input, user would need to re-select
        }
    }

     _onDragOver(event) {
          event.preventDefault();
          event.dataTransfer.dropEffect = 'copy';
          this.state.isDragging = true;
     }

     _onDragLeave(event) {
          if (!this.dropAreaRef.el.contains(event.relatedTarget)) {
             this.state.isDragging = false;
          }
     }

     _onDrop(event) {
          event.preventDefault();
          this.state.isDragging = false;
          const files = event.dataTransfer.files;
          if (files.length > 0) {
               this._handleFileSelection(files);
               if (this.fileInputRef.el) { // Try to assign to the input for form submission
                   this.fileInputRef.el.files = files;
               }
          }
     }

    _onFileChange(event) {
        const files = event.target.files;
        if (files.length > 0) {
            this._handleFileSelection(files);
        }
        // Don't clear event.target.value here if parent form relies on this input directly.
        // If this component were uploading via AJAX, then clearing it is fine.
    }

     _formatFileSize(bytes) {
         if (bytes === 0) return '0 Bytes';
         const k = 1024;
         const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
         const i = Math.floor(Math.log(bytes) / Math.log(k));
         return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
     }
}

FileUploaderComponent.template = "influence_gen_portal.FileUploaderComponentTemplate";
FileUploaderComponent.props = {
    acceptedFileTypes: { type: String, optional: true },
    maxFileSize: { type: Number, optional: true }, // in bytes
    fieldName: { type: String, optional: true, default: "files" }, // Name for the input field
    multiple: { type: Boolean, optional: true, default: false },
    label: { type: String, optional: true, default: _t("Upload File(s)") },
    id: { type: String, optional: true, default: "fileUploader" }, // Unique ID for label targeting
};

FileUploaderComponent.services = ["notification"];