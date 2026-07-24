/**
  Frontend validation for the Obituary Management Platform.
 
  This script provides client-side validation for the obituary submission form.
  Validation is performed on form submission and provides inline error messages
  next to each field. Supports text field validation and optional image file
  validation (type and size checks).
 */

(function () {
    "use strict";

    const form = document.getElementById("obituary-form");

    if (!form) {
        // No form on this page, exit early
        return;
    }

    // Field references
    const nameInput = document.getElementById("name");
    const dobInput = document.getElementById("date_of_birth");
    const dodInput = document.getElementById("date_of_death");
    const contentTextarea = document.getElementById("content");
    const authorInput = document.getElementById("author");
    const imageInput = document.getElementById("image");

    // Error message elements
    const nameError = document.getElementById("name-error");
    const dobError = document.getElementById("dob-error");
    const dodError = document.getElementById("dod-error");
    const contentError = document.getElementById("content-error");
    const authorError = document.getElementById("author-error");
    const imageError = document.getElementById("image-error");

    // Allowed image MIME types
    const ALLOWED_IMAGE_TYPES = [
        "image/png", "image/jpeg", "image/gif", "image/webp", "image/bmp"
    ];
    const MAX_IMAGE_SIZE = 16 * 1024 * 1024; // 16 MB

    /**
     * Display an error message for a specific field.
     *
     * @param {HTMLElement} inputEl - The input element to mark as error.
     * @param {HTMLElement} errorEl - The error message element to update.
     * @param {string} message - The error message to display.
     */
    function showError(inputEl, errorEl, message) {
        if (inputEl) {
            inputEl.classList.add("error");
        }
        if (errorEl) {
            errorEl.textContent = message;
        }
    }

    /**
     * Clear the error state for a specific field.
     *
     * @param {HTMLElement} inputEl - The input element to clear.
     * @param {HTMLElement} errorEl - The error message element to clear.
     */
    function clearError(inputEl, errorEl) {
        if (inputEl) {
            inputEl.classList.remove("error");
        }
        if (errorEl) {
            errorEl.textContent = "";
        }
    }

    /**
     * Clear all field errors.
     */
    function clearAllErrors() {
        const fields = [
            { input: nameInput, error: nameError },
            { input: dobInput, error: dobError },
            { input: dodInput, error: dodError },
            { input: contentTextarea, error: contentError },
            { input: authorInput, error: authorError },
            { input: imageInput, error: imageError },
        ];

        fields.forEach(function (field) {
            clearError(field.input, field.error);
        });
    }

    /**
     * Validate the uploaded image file (if any).
     *
     * @returns {boolean} True if the image is valid or no image provided.
     */
    function validateImage() {
        if (!imageInput || !imageInput.files || imageInput.files.length === 0) {
            // No file selected - optional field, so it's valid
            return true;
        }

        const file = imageInput.files[0];

        // Check file type
        if (ALLOWED_IMAGE_TYPES.indexOf(file.type) === -1) {
            showError(
                imageInput,
                imageError,
                "Image must be PNG, JPG, JPEG, GIF, WebP, or BMP."
            );
            return false;
        }

        // Check file size
        if (file.size > MAX_IMAGE_SIZE) {
            showError(
                imageInput,
                imageError,
                "Image must be smaller than 16 MB."
            );
            return false;
        }

        return true;
    }

    /**
     * Validate the entire form.
     *
     * @returns {boolean} True if the form is valid, false otherwise.
     */
    function validateForm() {
        let isValid = true;

        // Clear previous errors
        clearAllErrors();

        // --- Validate Name ---
        const name = nameInput ? nameInput.value.trim() : "";
        if (!name) {
            showError(nameInput, nameError, "Full name is required.");
            isValid = false;
        } else if (name.length > 100) {
            showError(
                nameInput,
                nameError,
                "Name must not exceed 100 characters."
            );
            isValid = false;
        }

        // --- Validate Author ---
        const author = authorInput ? authorInput.value.trim() : "";
        if (!author) {
            showError(authorInput, authorError, "Author name is required.");
            isValid = false;
        } else if (author.length > 100) {
            showError(
                authorInput,
                authorError,
                "Author name must not exceed 100 characters."
            );
            isValid = false;
        }

        // --- Validate Date of Birth ---
        const dob = dobInput ? dobInput.value : "";
        if (!dob) {
            showError(dobInput, dobError, "Date of birth is required.");
            isValid = false;
        }

        // --- Validate Date of Death ---
        const dod = dodInput ? dodInput.value : "";
        if (!dod) {
            showError(dodInput, dodError, "Date of death is required.");
            isValid = false;
        }

        // --- Validate Date Logic (death after birth) ---
        if (dob && dod) {
            if (dod < dob) {
                showError(
                    dodInput,
                    dodError,
                    "Date of death cannot be earlier than date of birth."
                );
                isValid = false;
            }
        }

        // --- Validate Content ---
        const content = contentTextarea ? contentTextarea.value.trim() : "";
        if (!content) {
            showError(
                contentTextarea,
                contentError,
                "Obituary content is required."
            );
            isValid = false;
        } else if (content.length < 10) {
            showError(
                contentTextarea,
                contentError,
                "Obituary content must be at least 10 characters long."
            );
            isValid = false;
        }

        // --- Validate Image (if provided) ---
        if (!validateImage()) {
            isValid = false;
        }

        return isValid;
    }

    /**
     * Validate a single field on blur (when the user leaves the field).
     *
     * @param {Event} event - The blur event.
     */
    function validateField(event) {
        const input = event.target;
        const id = input.id;

        // Clear the field's error first
        switch (id) {
            case "name":
                clearError(nameInput, nameError);
                if (!input.value.trim()) {
                    showError(nameInput, nameError, "Full name is required.");
                } else if (input.value.length > 100) {
                    showError(
                        nameInput,
                        nameError,
                        "Name must not exceed 100 characters."
                    );
                }
                break;

            case "author":
                clearError(authorInput, authorError);
                if (!input.value.trim()) {
                    showError(
                        authorInput,
                        authorError,
                        "Author name is required."
                    );
                } else if (input.value.length > 100) {
                    showError(
                        authorInput,
                        authorError,
                        "Author name must not exceed 100 characters."
                    );
                }
                break;

            case "date_of_birth":
                clearError(dobInput, dobError);
                if (!input.value) {
                    showError(dobInput, dobError, "Date of birth is required.");
                } else {
                    // Check date logic if death date is already filled
                    const dod = dodInput ? dodInput.value : "";
                    if (dod && dod < input.value) {
                        showError(
                            dodInput,
                            dodError,
                            "Date of death cannot be earlier than date of birth."
                        );
                    }
                }
                break;

            case "date_of_death":
                clearError(dodInput, dodError);
                if (!input.value) {
                    showError(dodInput, dodError, "Date of death is required.");
                } else {
                    const dob = dobInput ? dobInput.value : "";
                    if (dob && input.value < dob) {
                        showError(
                            dodInput,
                            dodError,
                            "Date of death cannot be earlier than date of birth."
                        );
                    }
                }
                break;

            case "content":
                clearError(contentTextarea, contentError);
                if (!input.value.trim()) {
                    showError(
                        contentTextarea,
                        contentError,
                        "Obituary content is required."
                    );
                } else if (input.value.trim().length < 10) {
                    showError(
                        contentTextarea,
                        contentError,
                        "Obituary content must be at least 10 characters long."
                    );
                }
                break;
        }
    }

    // --- Attach event listeners ---

    // Validate on form submission
    form.addEventListener("submit", function (event) {
        if (!validateForm()) {
            event.preventDefault();
            // Focus the first error field
            const firstErrorField = form.querySelector(".error");
            if (firstErrorField) {
                firstErrorField.focus();
            }
        }
    });

    // Validate text fields on blur
    const textInputs = form.querySelectorAll("input:not([type='file']), textarea");
    textInputs.forEach(function (input) {
        input.addEventListener("blur", validateField);
    });

    // Validate image on file selection change
    if (imageInput) {
        imageInput.addEventListener("change", function () {
            clearError(imageInput, imageError);
            validateImage();
        });
    }

    // Clear errors when user starts typing in a field
    textInputs.forEach(function (input) {
        input.addEventListener("input", function () {
            const id = input.id;
            switch (id) {
                case "name":
                    clearError(nameInput, nameError);
                    break;
                case "author":
                    clearError(authorInput, authorError);
                    break;
                case "date_of_birth":
                    clearError(dobInput, dobError);
                    break;
                case "date_of_death":
                    clearError(dodInput, dodError);
                    break;
                case "content":
                    clearError(contentTextarea, contentError);
                    break;
            }
        });
    });

    // Handle reset button
    const resetBtn = document.getElementById("reset-btn");
    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            // Allow form reset, then clear all validation errors
            setTimeout(clearAllErrors, 50);
        });
    }
})();
