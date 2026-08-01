document.addEventListener("DOMContentLoaded", () => {
    // ==========================================
    // DOM ELEMENTS
    // ==========================================
    // Windows
    const setupWindow = document.getElementById("setup-window");
    const loreWindow = document.getElementById("lore-window");
    
    // Form Inputs
    const form = document.getElementById("lore-form");
    const charName = document.getElementById("char-name");
    const charClass = document.getElementById("char-class");
    const charGender = document.getElementById("char-gender");
    const charLocation = document.getElementById("char-location");
    const charAge = document.getElementById("char-age");
    const charAlignment = document.getElementById("char-alignment");
    const charDesc = document.getElementById("char-desc");
    const spritePreview = document.getElementById("sprite-preview");
    
    // Buttons
    const generateBtn = document.getElementById("generate-btn");
    const pdfBtn = document.getElementById("pdf-btn");
    const backBtn = document.getElementById("back-btn");
    const retryBtn = document.getElementById("retry-btn");
    
    // Output Elements
    const outName = document.getElementById("out-name");
    const outClass = document.getElementById("out-class");
    const outGender = document.getElementById("out-gender");
    const outLocation = document.getElementById("out-location");
    const outRole = document.getElementById("out-role");
    const outDesc = document.getElementById("out-desc");
    const outAct1 = document.getElementById("out-act1");
    const outAct2 = document.getElementById("out-act2");
    const outAct3 = document.getElementById("out-act3");
    const outAct4 = document.getElementById("out-act4");
    const outMetadata = document.getElementById("out-metadata");

    // ==========================================
    // STATE & ASSETS
    // ==========================================
    let currentLoreData = null; // Holds the latest generated lore payload for the PDF endpoint


    // ==========================================
    // VALIDATIONS
    // ==========================================

    const ageInput = document.getElementById('char-age');

    // 1. Prevent typing the minus sign or 'e' (for exponents) entirely
    ageInput.addEventListener('keydown', function(e) {
        if (e.key === '-' || e.key === 'e' || e.key === 'E' || e.key === '+' || e.key === '.') {
            e.preventDefault();
        }
    });

    // 2. Clamp the value if they paste in a massive number or try to bypass limits
    ageInput.addEventListener('input', function() {
        if (this.value !== '') {
            // Force it to be an integer
            let val = parseInt(this.value, 10);
            
            // Clamp between 0 and 2000
            if (val < 0) this.value = 0;
            if (val > 2000) this.value = 2000;
        }
    });

    // ==========================================
    // TOAST NOTIFICATION LOGIC
    // ==========================================
    function showToast(message) {
        // Create the toast element
        const toast = document.createElement("div");
        toast.textContent = message;
        
        // Apply inline styles (you can also move these to your ro-theme.css as a .toast class)
        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.backgroundColor = "rgba(220, 53, 69, 0.95)"; // A nice error red
        toast.style.color = "white";
        toast.style.padding = "12px 24px";
        toast.style.borderRadius = "4px";
        toast.style.boxShadow = "0 4px 6px rgba(0,0,0,0.3)";
        toast.style.zIndex = "9999";
        toast.style.transition = "opacity 0.3s ease";
        toast.style.opacity = "1";
        
        // Add to body
        document.body.appendChild(toast);
        
        // Fade out and remove after 3 seconds
        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => toast.remove(), 300); // Wait for fade transition
        }, 3000);
    }

    // ==========================================
    // INITIALIZATION (Fetch Options)
    // ==========================================
    async function loadOptions() {
        try {
            const response = await fetch('/api/options');
            if (!response.ok) throw new Error("Failed to fetch options");
            
            const data = await response.json();
            
            // Populate select fields dynamically
            populateSelect(charClass, data.classes, "Select Class");
            populateSelect(charGender, data.genders, "Select Gender");
            populateSelect(charLocation, data.locations, "Any Location");
            populateSelect(charAlignment, data.alignments, "Any Alignment");

        } catch (error) {
            console.error("Error loading options:", error);
            showToast("Something went wrong. Please contact the admin.");
            // Fallbacks to hardcoded HTML if backend is unreachable on load
        }
    }

    function populateSelect(selectElement, optionsArray, defaultText) {
        selectElement.innerHTML = `<option value="" ${defaultText.includes('Select') ? 'disabled' : ''} selected>${defaultText}</option>`;
        optionsArray.forEach(opt => {
            const option = document.createElement("option");
            option.value = opt;
            option.textContent = opt;
            selectElement.appendChild(option);
        });
    }

    // ==========================================
    // SPRITE PREVIEW LOGIC
    // ==========================================
    function updateSprite() {
        const selectedClass = charClass.value;

        if (selectedClass) {
            // Formats "Swordsman" to "swordsman.png" to match your folder
            const assetName = `${selectedClass.toLowerCase()}.png`;
            
            // Replaces the placeholder text with the actual image tag
            spritePreview.innerHTML = `
                <img 
                    src="assets/sprites/${assetName}" 
                    alt="${selectedClass} Class Sprite" 
                    style="max-width: 250px; max-height: 250px; object-fit: contain; image-rendering: pixelated;"
                >
            `;
        } else {
            // Fallback if they somehow deselect a class
            spritePreview.innerHTML = '<p class="sprite-placeholder">No Class<br>Selected</p>';
        }
    }

    if (charClass) charClass.addEventListener("change", updateSprite);
    if (charGender) charGender.addEventListener("change", updateSprite);

    // ==========================================
    // GENERATE LORE (API Call)
    // ==========================================
    async function generateLore(isRetry = false) {
        
        // Validate required fields if not a retry
        if (!isRetry && (!form.checkValidity() || !charClass.value || !charGender.value)) {
            form.reportValidity();
            return;
        }

        // Prepare payload matching CharacterLoreCreationRequest model
        const requestPayload = {
            character_name: charName.value.trim() || undefined,
            character_class: charClass.value,
            gender: charGender.value,
            birth_location: charLocation.value || undefined,
            character_age: charAge.value ? parseInt(charAge.value, 10) : undefined,
            character_alignment: charAlignment.value || undefined,
            description: charDesc.value.trim() || undefined
        };

        // UI Loading State
        const originalBtnText = isRetry ? retryBtn.textContent : generateBtn.textContent;
        const activeBtn = isRetry ? retryBtn : generateBtn;
        
        activeBtn.textContent = "Casting Spell...";
        activeBtn.disabled = true;
        document.body.style.cursor = "wait";

        try {
            const response = await fetch('/api/generate-lore', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestPayload)
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            currentLoreData = data; // Save for PDF generation
            
            renderLoreWindow(data);
            
            // Swap windows
            setupWindow.classList.add("hidden");
            loreWindow.classList.remove("hidden");

            document.querySelector('.parchment-scroll').scrollTop = 0;

        } catch (error) {
            console.error("Error generating lore:", error);
            showToast("The Server-side spell failed to cast. Check the console for details.");
        } finally {
            // Restore UI State
            activeBtn.textContent = originalBtnText;
            activeBtn.disabled = false;
            document.body.style.cursor = "default";
        }
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        generateLore(false);
    });

    retryBtn.addEventListener("click", () => {
        generateLore(true);
    });

    // ==========================================
    // RENDER OUTPUT DATA
    // ==========================================
    function renderLoreWindow(data) {
        outName.textContent = data.name || "Unknown";
        outClass.textContent = data.class || "Unknown";
        outGender.textContent = data.gender || "Unknown";
        outLocation.textContent = data.place_of_birth || "Unknown";
        
        outRole.textContent = data.role || "No role provided.";
        outDesc.textContent = data.description || "No description provided.";
        
        outAct1.textContent = data.act_1 || "";
        outAct2.textContent = data.act_2 || "";
        outAct3.textContent = data.act_3 || "";
        outAct4.textContent = data.act_4 || "";
        
        // Format metadata JSON nicely
        try {
            const metaObj = typeof data.metadata === 'string' ? JSON.parse(data.metadata) : data.metadata;
            outMetadata.textContent = JSON.stringify(metaObj, null, 2);
        } catch (e) {
            outMetadata.textContent = data.metadata || "{}";
            console.error(e)
            //showToast("Something went wrong. Please contact the admin.");
        }
    }

    // ==========================================
    // PDF GENERATION (API Call)
    // ==========================================
    pdfBtn.addEventListener("click", async () => {
        if (!currentLoreData) return;

        pdfBtn.textContent = "Scribing Parchment...";
        pdfBtn.disabled = true;

        try {
            const response = await fetch('/api/generate-pdf', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentLoreData)
            });

            if (!response.ok) throw new Error("Failed to generate PDF");

            // Handle file download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            
            // Extract filename from headers if possible, or fallback
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = `${currentLoreData.name || 'Character'}_Lore.pdf`;
            if (contentDisposition && contentDisposition.includes('filename=')) {
                filename = contentDisposition.split('filename=')[1].replace(/"/g, '');
            }

            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
            
        } catch (error) {
            console.error("Error downloading PDF:", error);
            showToast("Something went wrong. Please contact the admin.");
        } finally {
            pdfBtn.textContent = "Save as PDF";
            pdfBtn.disabled = false;
        }
    });

    // ==========================================
    // NAVIGATION
    // ==========================================
    backBtn.addEventListener("click", () => {
        loreWindow.classList.add("hidden");
        setupWindow.classList.remove("hidden");
        
        // Optional: scroll to top
        document.querySelector('.desktop-environment').scrollTop = 0;
    });

    // Initialize the app on load
    loadOptions();
});