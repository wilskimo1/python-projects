document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Script.js loaded successfully!");

    let eventListenersAttached = false; // Track if listeners are attached
    let isSending = false; // Prevent duplicate chatbot requests

    // 🟢 Navbar Toggle
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.getElementById("navbarNav");

    if (navbarToggler && navbarCollapse) {
        console.log("✅ Navbar elements found!");
        document.querySelectorAll(".nav-link").forEach(link => {
            link.addEventListener("click", function () {
                if (window.innerWidth < 992) {
                    new bootstrap.Collapse(navbarCollapse).hide();
                }
            });
        });
    } else {
        console.error("❌ ERROR: Navbar elements NOT found!");
    }

    // 🟢 Fetch all projects for Projects Page
    const projectsContainer = document.getElementById("projects-container");
    if (projectsContainer) {
        console.log("📂 Fetching projects...");
        fetch("/api/projects")
            .then(response => response.json())
            .then(projects => {
                projectsContainer.innerHTML = "";
                projects.forEach(project => {
                    projectsContainer.innerHTML += `
                        <div class="col-md-4 mb-4">
                            <a href="/projects/${project.id}" class="text-decoration-none text-dark">
                                <div class="card project-card shadow-sm">
                                    <div class="card-body">
                                        <h3 class="card-title">${project.title}</h3>
                                        <p><strong>Technologies:</strong> ${project.technologies}</p>
                                        <p>${project.short_description}</p>
                                        <button class="btn btn-outline-primary mt-2">Learn More</button>
                                    </div>
                                </div>
                            </a>
                        </div>
                    `;
                });
                console.log("✅ Projects loaded successfully!");
            })
            .catch(error => console.error("❌ Error fetching projects:", error));
    }
});

 // 🟢 Fetch Project Details for Project Details Page
 if (document.getElementById("project-title")) {
    console.log("📂 Fetching project details...");
    const projectId = window.location.pathname.split("/").pop(); // Extract project ID from URL

    fetch(`/api/projects/${projectId}`)
        .then(response => response.json())
        .then(project => {
            if (project.error) {
                console.error("❌ Error: Project not found");
                document.getElementById("project-title").innerText = "Project Not Found";
                return;
            }

            // Populate project details dynamically
            document.getElementById("project-title").innerText = project.title;
            document.getElementById("project-technologies").innerHTML = `<strong>Technologies Used:</strong> ${project.technologies}`;
            document.getElementById("project-description").innerText = project.detailed_description;
            document.getElementById("project-use-case").innerText = project.commercial_use_case;

            // Show deployment guide for "flask-aws-deployment" project only
           // if (project.id === "flask-aws-deployment") {
            //    document.getElementById("deployment-guide").style.display = "block";
           // }

            console.log("✅ Project details loaded successfully!");
        })
        .catch(error => console.error("❌ Error fetching project details:", error));
}
    // 🟢 Fetch and display GitHub commits
    const commitsContainer = document.getElementById("github-commits");
    if (commitsContainer) {
        console.log("📂 Fetching latest GitHub commits...");
        function fetchGitHubCommits() {
            fetch("/api/github-commits")
                .then(response => response.json())
                .then(commits => {
                    commitsContainer.innerHTML = commits.error
                    ? `<li class="list-group-item text-danger">${commits.error}</li>`
                    : commits.map(commit => `
                        <li class="list-group-item">
                            <strong>${commit.message}</strong><br>
                            <small>By: ${commit.author} on ${new Date(commit.date).toLocaleString()}</small>
                        </li>
                    `).join("");               
                    console.log("✅ GitHub commits loaded successfully!");
                })
                .catch(error => {
                    console.error("❌ Error fetching GitHub commits:", error);
                    commitsContainer.innerHTML = `<li class="list-group-item text-danger">Failed to load commits.</li>`;
                });
        }
        fetchGitHubCommits();
        document.getElementById("refreshCommits")?.addEventListener("click", fetchGitHubCommits);
    }

     // 🟢 AWS Certifications
     const certContainer = document.getElementById("certifications-container");
     if (certContainer) {
         console.log("🎓 Loading AWS Certifications...");
 
         const certifications = [
             { id: "952f0071-5974-4753-9487-a7b47566859c" },
             { id: "8d927d2f-3ae9-42a8-a545-c1cb5f94975e" },
             { id: "e91dc156-f68b-4e50-a677-bae2e41c0c8f" },
             { id: "0598dd26-4893-4ff4-a8c1-3d0185ddddb7" },
             { id: "1f308bfe-d638-4840-9925-56440d9ea6c2" }
         ];
 
         certifications.forEach(cert => {
             const certDiv = document.createElement("div");
             certDiv.classList.add("col-md-3", "mb-4", "text-center");
             certDiv.innerHTML = `
                 <div data-iframe-width="150" data-iframe-height="270"
                     data-share-badge-id="${cert.id}" data-share-badge-host="https://www.credly.com">
                 </div>
             `;
             certContainer.appendChild(certDiv);
         });
 
         // Load Credly Embed Script
         const script = document.createElement("script");
         script.type = "text/javascript";
         script.src = "//cdn.credly.com/assets/utilities/embed.js";
         script.async = true;
         document.body.appendChild(script);
 
         console.log("✅ AWS Certifications loaded successfully!");
     }


    // 🟢 Serverless Chatbot Integration
    function sendMessage() {
        if (isSending) return;
        isSending = true;

        let userInputField = document.getElementById("user-input");
        let userInput = userInputField.value.trim();
        let chatBox = document.getElementById("chat-box");

        if (!userInput) {
            isSending = false;
            return;
        }

        chatBox.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;

        fetch("/api/chatbot", {
            method: "POST",
            body: JSON.stringify({ message: userInput }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += `<div><strong>Bot:</strong> ${data.response || "No response from chatbot."}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            userInputField.value = "";
            isSending = false;
        })
        .catch(error => {
            console.error("❌ Fetch Error:", error);
            chatBox.innerHTML += `<div><strong>Error:</strong> Failed to connect to chatbot.</div>`;
            isSending = false;
        });
    }

    if (window.location.pathname.includes("serverless-chatbot")) {
        console.log("🟢 Chatbot page detected.");
        let sendButton = document.getElementById("send-btn");
        let userInput = document.getElementById("user-input");

        if (sendButton && userInput && !eventListenersAttached) {
            sendButton.addEventListener("click", sendMessage);
            userInput.addEventListener("keypress", function (event) {
                if (event.key === "Enter") sendMessage();
            });
            eventListenersAttached = true;
            console.log("✅ Chatbot event listeners attached.");
        }
    }

    function attachContactFormListener() {
        const contactForm = document.getElementById("contactForm");
        const successMessage = document.getElementById("successMessage");
    
        // ✅ If the contact form does NOT exist, don't log a warning
        if (!contactForm) {
            console.log("ℹ️ Contact form not found on this page. Skipping listener setup.");
            return; // ⛔ Exit early, don't set up MutationObserver
        }
    
        console.log("📩 Contact form detected. Attaching event listener...");
        attachEventListenerToContactForm(contactForm, successMessage);
    }
    
// ✅ Function to attach event listener once the form is available
function attachEventListenerToContactForm(contactForm, successMessage) {
    contactForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("name")?.value.trim();
        const email = document.getElementById("email")?.value.trim();
        const message = document.getElementById("message")?.value.trim();

        if (!name || !email || !message) {
            alert("⚠️ Please fill in all fields.");
            return;
        }

        // Send data to Flask backend
        fetch("/send-message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, email, message }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("📨 Response from server:", data); // <-- Add this
            if (data.success) {
                successMessage.style.display = "block";
                setTimeout(() => {
                    successMessage.style.display = "none";
                }, 3000);
                contactForm.reset();
            } else {
                alert("❌ Failed to send message: " + data.error);
            }
        })
        .catch((error) => {
            console.error("❌ Error sending message:", error);
            alert("⚠️ There was an error sending your message.");
        });
    });

    console.log("✅ Contact form event listener attached.");
}

    
// ✅ Call function after DOM is loaded
document.addEventListener("DOMContentLoaded", attachContactFormListener);  

 // ✅ Ensure Random Number Button Works
 const randomButton = document.getElementById("random-btn");
 const resultDisplay = document.getElementById("random-result");

 if (randomButton && resultDisplay) {
     console.log("🎲 Random number button found!");
     randomButton.addEventListener("click", function () {
         console.log("🔄 Fetching random number from API...");
         fetch("/api/random-number")
             .then(response => response.json())
             .then(data => {
                 console.log("✅ API Response:", data);
                 resultDisplay.innerText = `Your random number is: ${data.random_number}`;
             })
             .catch(error => console.error("❌ Error fetching random number:", error));
     });
 }


 // Allow pressing "Enter" in any field to trigger the search
 document.querySelectorAll(".weather-input").forEach(input => {
     input.addEventListener("keypress", function (event) {
         if (event.key === "Enter") {
             event.preventDefault(); // Prevent form submission
             fetchWeather();
         }
     });
 });


 function fetchWeather() {
     console.log("🔍 Fetching weather...");

     const city = document.getElementById("city-input").value.trim();
     const state = document.getElementById("state-input").value.trim().toUpperCase();
     const zip = document.getElementById("zip-input").value.trim();
     const country = document.getElementById("country-input").value.trim().toUpperCase() || "US";

     let url = "/weather?";

     if (zip) {
         url += `zip=${zip},${country}`;
     } else if (city && state) {
         url += `city=${city}&state=${state}&country=${country}`;
     } else if (city) {
         url += `city=${city}&country=${country}`;
     } else {
         alert("⚠️ Please enter a city and state or a zip code.");
         return;
     }

     console.log(`🌍 API Request URL: ${url}`);

     fetch(url)
         .then(response => response.json())
         .then(data => {
             if (data.error) {
                 alert(`❌ ${data.error}`);
                 return;
             }

             document.getElementById("weather-city").innerText = `📍 City: ${data.city}, ${data.country}`;
             document.getElementById("weather-temp").innerText = `🌡️ Temperature: ${data.temperature}°F`;
             document.getElementById("weather-low-high").innerText = `🔻 Low: ${data.temp_min}°F | 🔺 High: ${data.temp_max}°F`;
             document.getElementById("weather-humidity").innerText = `💧 Humidity: ${data.humidity}%`;
             document.getElementById("weather-description").innerText = `☁️ Description: ${data.weather}`;

             const iconUrl = `https://openweathermap.org/img/wn/${data.icon}.png`;
             const weatherIcon = document.getElementById("weather-icon");
             weatherIcon.src = iconUrl;
             weatherIcon.style.display = "inline"; // Show the weather icon
         })
         .catch(error => console.error("❌ Error fetching weather data:", error));
 };


    // 🟢 Fetch Files for S3 File Manager
    function fetchFiles() {
        console.log("📂 Fetching files from S3...");
        fetch("/api/s3/list")
            .then(response => response.json())
            .then(data => {
                const fileTable = document.getElementById("fileTable");
                if (!fileTable) return console.error("❌ ERROR: fileTable not found in DOM.");

                fileTable.innerHTML = data.length === 0
                    ? `<tr><td colspan="3" class="text-center">No files found.</td></tr>`
                    : data.map(file => `
                        <tr>
                            <td><a href="${file.url}" target="_blank">${file.name}</a></td>
                            <td>${(file.size / 1024).toFixed(2)} KB</td>
                            <td><button class="btn btn-danger btn-sm" onclick="deleteFile('${file.name}')">Delete</button></td>
                        </tr>
                    `).join("");
            })
            .catch(error => console.error("❌ Error fetching S3 files:", error));
    }

    if (window.location.pathname === "/s3-file-manager") {
        fetchFiles();
    }

    // 🟢 Upload File to S3
    window.uploadFile = function () {
        const fileInput = document.getElementById("fileInput");
        const file = fileInput.files[0];

        if (!file) return alert("⚠️ Please select a file before uploading.");

        let formData = new FormData();
        formData.append("file", file);

        fetch("/api/s3/upload", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`❌ Upload failed: ${data.error}`);
            } else {
                alert("✅ File uploaded successfully!");
                fetchFiles();
            }
        })
        .catch(error => {
            console.error("❌ Network/Fetch Error:", error);
            alert("❌ Upload request failed. Check console for details.");
        });
    };

    // 🟢 Delete File from S3
    window.deleteFile = function (fileName) {
        fetch("/api/s3/delete", {
            method: "POST",
            body: JSON.stringify({ file_name: fileName }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`❌ Delete failed: ${data.error}`);
            } else {
                alert("✅ File deleted successfully!");
                fetchFiles();
            }
        })
        .catch(error => {
            console.error("❌ Network/Fetch Error:", error);
            alert("❌ Delete request failed. Check console for details.");
    });
};