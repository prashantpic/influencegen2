odoo.define('influence_gen_portal.FileUploaderComponent', function (require) {
    'use strict';

    const { Component, useState, useRef, onMounted, onWillUnmount } = owl;
    const { _t } = require('web.core');
    const rpc = require('web.rpc'); // Using Odoo's global RPC for simplicity, could use a service

    class FileUploaderComponent extends Component {
        static template = 'influence_gen_portal.FileUploaderComponentTemplate';
        static props = {
            acceptedFileTypes: { type: String, optional: false }, // e.g., "image/jpeg,image/png,.pdf"
            maxFileSize: { type: Number, optional: true, default: 5 * 1024 * 1024 }, // 5MB
            uploadUrl: { type: String, optional: false }, // Backend URL for upload
            fieldName: { type: String, optional: false }, // Field name for the backend
            multiple: { type: Boolean, optional: true, default: false },
            label: { type: String, optional: true, default: _t("Upload File(s)") },
            parentFormInputId: { type: String, optional: true }, // ID of a hidden input in parent form to store attachment IDs
            onUploadSuccess: { type: Function, optional: true},
            onUploadError: { type: Function, optional: true},
            onFileRemoved: { type: Function, optional: true},
        };

        setup() {
            this.state = useState({
                selectedFiles: [], // { file: File, name: String, size: Number, type: String, status: String, progress: Number, errorMessage: String, serverId: null }
                isDragging: false,
            });

            this.fileInputRef = useRef('fileInput');
            this.dropZoneRef = useRef('dropZone');

            this.handleDragOver = this.handleDragOver.bind(this);
            this.handleDragLeave = this.handleDragLeave.bind(this);
            this.handleDrop = this.handleDrop.bind(this);
            this.handleFileChange = this.handleFileChange.bind(this);

            onMounted(() => {
                if (this.dropZoneRef.el) {
                    this.dropZoneRef.el.addEventListener('dragover', this.handleDragOver);
                    this.dropZoneRef.el.addEventListener('dragleave', this.handleDragLeave);
                    this.dropZoneRef.el.addEventListener('drop', this.handleDrop);
                }
            });

            onWillUnmount(() => {
                if (this.dropZoneRef.el) {
                    this.dropZoneRef.el.removeEventListener('dragover', this.handleDragOver);
                    this.dropZoneRef.el.removeEventListener('dragleave', this.handleDragLeave);
                    this.dropZoneRef.el.removeEventListener('drop', this.handleDrop);
                }
            });
        }

        handleDragOver(event) {
            event.preventDefault();
            this.state.isDragging = true;
        }

        handleDragLeave(event) {
            event.preventDefault();
            this.state.isDragging = false;
        }

        handleDrop(event) {
            event.preventDefault();
            this.state.isDragging = false;
            const files = event.dataTransfer.files;
            if (files.length) {
                this._addFilesToList(files);
            }
        }

        handleFileChange(event) {
            const files = event.target.files;
            if (files.length) {
                this._addFilesToList(files);
            }
            // Reset file input to allow selecting the same file again
            if (this.fileInputRef.el) {
                 this.fileInputRef.el.value = '';
            }
        }

        _addFilesToList(fileList) {
            const newFiles = [];
            for (let i = 0; i < fileList.length; i++) {
                const file = fileList[i];
                const validation = this._validateFile(file);
                if (validation.isValid) {
                    const fileObject = {
                        file: file,
                        name: file.name,
                        size: file.size,
                        type: file.type,
                        status: 'pending', // 'pending', 'uploading', 'success', 'error'
                        progress: 0,
                        errorMessage: null,
                        serverId: null, // To store ID from server on success
                    };
                    if (!this.props.multiple) {
                        this.state.selectedFiles.splice(0, this.state.selectedFiles.length); // Clear existing for single file
                    }
                    newFiles.push(fileObject);
                } else {
                     // Immediately show error for this file, or collect and show all
                    owl.Component.env.services.notification.add(
                        validation.errorMessage,
                        { type: 'danger', title: _t('Validation Error') }
                    );
                }
            }
            
            if (newFiles.length > 0) {
                 if (this.props.multiple) {
                    this.state.selectedFiles.push(...newFiles);
                } else {
                    this.state.selectedFiles = newFiles;
                }
                // Optionally auto-start upload
                newFiles.forEach(f => this.startUpload(f));
            }
        }

        _validateFile(file) {
            const acceptedTypes = this.props.acceptedFileTypes.split(',').map(t => t.trim().toLowerCase());
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            const fileMimeType = file.type.toLowerCase();

            let typeMatch = false;
            if (acceptedTypes.some(type => type.startsWith('.'))) { // Check extension
                if (acceptedTypes.includes(fileExtension)) {
                    typeMatch = true;
                }
            }
            if (!typeMatch && acceptedTypes.some(type => type.includes('/'))) { // Check MIME type
                 if (acceptedTypes.includes(fileMimeType)) {
                    typeMatch = true;
                 } else if (acceptedTypes.some(accepted => accepted.endsWith('/*') && fileMimeType.startsWith(accepted.slice(0, -1)))) {
                    typeMatch = true; // Wildcard match like image/*
                 }
            }
             if (!typeMatch && acceptedTypes.some(type => !type.startsWith('.') && !type.includes('/'))) {
                // This case is ambiguous, but we can assume it's a general type and perhaps allow if other checks pass
                // For now, strict matching on extension or full MIME type
             }


            if (!typeMatch) {
                return { isValid: false, errorMessage: _t("File type '%s' is not accepted. Accepted types: %s", file.type || fileExtension, this.props.acceptedFileTypes) };
            }

            if (file.size > this.props.maxFileSize) {
                return { isValid: false, errorMessage: _t("File '%s' is too large (%s). Maximum size is %s.", file.name, this._formatFileSize(file.size), this._formatFileSize(this.props.maxFileSize)) };
            }
            return { isValid: true };
        }

        async startUpload(fileObject) {
            if (fileObject.status !== 'pending' &amp;&amp; fileObject.status !== 'error') return;

            fileObject.status = 'uploading';
            fileObject.progress = 0;
            fileObject.errorMessage = null;

            const formData = new FormData();
            formData.append(this.props.fieldName, fileObject.file);
            formData.append('csrf_token', odoo.csrf_token); // Odoo global CSRF token

            try {
                // Using Odoo's RPC for upload to leverage session and CSRF handling, if applicable
                // This assumes uploadUrl is an Odoo controller route.
                // For raw XHR:
                const xhr = new XMLHttpRequest();
                xhr.open('POST', this.props.uploadUrl, true);
                
                // Odoo's CSRF token for non-RPC jQuery.ajax can be added as a header if needed
                // For simple POSTs via controller, Odoo handles CSRF if 'csrf_token' is in form data.
                
                xhr.upload.onprogress = (event) => {
                    if (event.lengthComputable) {
                        fileObject.progress = Math.round((event.loaded * 100) / event.total);
                    }
                };

                xhr.onload = () => {
                    if (xhr.status >= 200 &amp;&amp; xhr.status < 300) {
                        const response = JSON.parse(xhr.responseText);
                        if (response.error) {
                            fileObject.status = 'error';
                            fileObject.errorMessage = response.error.message || _t("Unknown server error.");
                            if (this.props.onUploadError) this.props.onUploadError(fileObject, response.error);
                        } else {
                            fileObject.status = 'success';
                            fileObject.progress = 100;
                            fileObject.serverId = response.id || response.attachment_id || null; // Assuming server returns ID
                            if (this.props.onUploadSuccess) this.props.onUploadSuccess(fileObject, response);
                            this._updateParentFormInput();
                        }
                    } else {
                        fileObject.status = 'error';
                        fileObject.errorMessage = _t("Upload failed. Server responded with status %s.", xhr.status);
                        if (this.props.onUploadError) this.props.onUploadError(fileObject, {message: fileObject.errorMessage});
                    }
                };

                xhr.onerror = () => {
                    fileObject.status = 'error';
                    fileObject.errorMessage = _t("Network error during upload.");
                     if (this.props.onUploadError) this.props.onUploadError(fileObject, {message: fileObject.errorMessage});
                };
                
                xhr.send(formData);

            } catch (error) {
                console.error("Upload error:", error);
                fileObject.status = 'error';
                fileObject.errorMessage = error.message || _t("An unexpected error occurred during upload.");
                if (this.props.onUploadError) this.props.onUploadError(fileObject, error);
            }
        }

        removeFile(fileObject) {
            const index = this.state.selectedFiles.indexOf(fileObject);
            if (index > -1) {
                this.state.selectedFiles.splice(index, 1);
                // If there's an XHR associated, abort it (more complex to track here)
                // For now, just remove from list. If serverId exists, might need to inform server.
                if (this.props.onFileRemoved) this.props.onFileRemoved(fileObject);
                this._updateParentFormInput();
            }
        }
        
        _updateParentFormInput() {
            if (this.props.parentFormInputId) {
                const inputEl = document.getElementById(this.props.parentFormInputId);
                if (inputEl) {
                    const successfulUploadIds = this.state.selectedFiles
                        .filter(f => f.status === 'success' &amp;&amp; f.serverId)
                        .map(f => f.serverId);
                    inputEl.value = successfulUploadIds.join(',');
                }
            }
        }

        _formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        triggerFileInput() {
            if (this.fileInputRef.el) {
                this.fileInputRef.el.click();
            }
        }
    }

    if (odoo.influence_gen_portal &amp;&amp; odoo.influence_gen_portal.components) {
        odoo.influence_gen_portal.components.FileUploaderComponent = FileUploaderComponent;
    } else {
        // Fallback or error if namespace doesn't exist. This assumes a global setup.
        // For direct registration as an OWL component in an Odoo view:
        // Component.env.componentCollector.add("influence_gen_portal.FileUploaderComponent", FileUploaderComponent);
        // This is typically handled by Odoo's asset system when components are in assets_qweb.
    }


    return FileUploaderComponent;
});