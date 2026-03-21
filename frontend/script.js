// ============================================================
// BACKEND URL — change this after you deploy to Render
// ============================================================
const BACKEND_URL = "https://YOUR-BACKEND.onrender.com";

// ============================================================
// EDUCATION PATH LOGIC
// ============================================================
const pathConfigs = {
  A: ["10th", "12th", "UG", "PG"],
  B: ["10th", "Diploma", "UG", "PG"],
  C: ["10th", "ITI", "Diploma", "UG", "PG"]
};

let selectedPath = null;

function switchPath(path) {
  selectedPath = path;
  renderEducationEntries(pathConfigs[path]);
}

function renderEducationEntries(levels) {
  const container = document.getElementById("education-entries");
  container.innerHTML = "";

  levels.forEach((level, i) => {
    const isOptional = (level === "PG");
    const showBacklogs = ["UG", "PG", "Diploma"].includes(level);
    const showStream = !["10th", "ITI"].includes(level);

    container.innerHTML += `
      <div class="edu-card">
        <h3>${level} ${isOptional ? "(Optional)" : "*"}</h3>
        <input type="hidden" id="edu-level-${i}" value="${level}"/>
        <div class="form-row">
          <div class="form-group">
            <label>Board / University *</label>
            <input type="text" id="edu-board-${i}" placeholder="e.g. CBSE, Mumbai University"/>
          </div>
          ${showStream ? `
          <div class="form-group">
            <label>Stream / Specialization *</label>
            <input type="text" id="edu-stream-${i}" placeholder="e.g. Science, CSE"/>
          </div>` : `<div></div>`}
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Year of Passing *</label>
            <input type="number" id="edu-year-${i}" placeholder="e.g. 2022" min="1990" max="${new Date().getFullYear()}"/>
          </div>
          <div class="form-group">
            <label>Score *</label>
            <input type="number" id="edu-score-${i}" placeholder="e.g. 85 or 8.5" step="0.01"/>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Score Scale *</label>
            <select id="edu-scale-${i}">
              <option value="percentage">Percentage (%)</option>
              <option value="cgpa10">CGPA (out of 10)</option>
              <option value="cgpa4">CGPA (out of 4)</option>
              <option value="grade">Grade</option>
            </select>
          </div>
          ${showBacklogs ? `
          <div class="form-group">
            <label>Backlog Count</label>
            <input type="number" id="edu-backlogs-${i}" placeholder="0" min="0" value="0"/>
          </div>` : `<div></div>`}
        </div>
        <div class="form-group">
          <label>Gap After This Level (months)</label>
          <input type="number" id="edu-gap-${i}" placeholder="0" min="0" value="0"/>
        </div>
        <span class="error" id="err-edu-${i}"></span>
      </div>
    `;
  });
}

// ============================================================
// WORK EXPERIENCE LOGIC
// ============================================================
let workCount = 0;

function addWorkEntry() {
  const container = document.getElementById("work-entries");
  const i = workCount++;

  container.innerHTML += `
    <div class="work-card" id="work-card-${i}">
      <h3>Work Entry ${i + 1} <button class="btn-remove" onclick="removeWork(${i})">✕ Remove</button></h3>
      <div class="form-row">
        <div class="form-group">
          <label>Company Name *</label>
          <input type="text" id="work-company-${i}" placeholder="e.g. Infosys"/>
        </div>
        <div class="form-group">
          <label>Designation *</label>
          <input type="text" id="work-designation-${i}" placeholder="e.g. Software Engineer"/>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Domain / Industry *</label>
          <select id="work-domain-${i}">
            <option value="">-- Select --</option>
            <option value="IT">IT</option>
            <option value="Non-IT">Non-IT</option>
            <option value="Government">Government</option>
            <option value="Startup">Startup</option>
            <option value="Freelance">Freelance</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div class="form-group">
          <label>Employment Type *</label>
          <select id="work-type-${i}">
            <option value="">-- Select --</option>
            <option value="Full-time">Full-time</option>
            <option value="Part-time">Part-time</option>
            <option value="Internship">Internship</option>
            <option value="Contract">Contract</option>
            <option value="Freelance">Freelance</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Start Date *</label>
          <input type="month" id="work-start-${i}"/>
        </div>
        <div class="form-group">
          <label>End Date (leave blank if current)</label>
          <input type="month" id="work-end-${i}"/>
          <small style="color:#888">Leave blank if currently working here</small>
        </div>
      </div>
      <div class="form-group">
        <label>Key Skills Used</label>
        <input type="text" id="work-skills-${i}" placeholder="e.g. Python, React, SQL (comma separated)"/>
      </div>
    </div>
  `;
}

function removeWork(i) {
  const card = document.getElementById(`work-card-${i}`);
  if (card) card.remove();
}

// ============================================================
// COLLECT FORM DATA
// ============================================================
function collectFormData() {
  const path = selectedPath;
  const levels = path ? pathConfigs[path] : [];

  // Personal info
  const personal = {
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    dob: document.getElementById("dob").value,
  };

  // Education entries
  const education = levels.map((level, i) => ({
    level: level,
    board: document.getElementById(`edu-board-${i}`)?.value.trim() || "",
    stream: document.getElementById(`edu-stream-${i}`)?.value.trim() || "",
    yearOfPassing: parseInt(document.getElementById(`edu-year-${i}`)?.value) || null,
    score: parseFloat(document.getElementById(`edu-score-${i}`)?.value) || null,
    scoreScale: document.getElementById(`edu-scale-${i}`)?.value || "percentage",
    backlogs: parseInt(document.getElementById(`edu-backlogs-${i}`)?.value) || 0,
    gapAfter: parseInt(document.getElementById(`edu-gap-${i}`)?.value) || 0,
  }));

  // Work entries
  const workEntries = [];
  for (let i = 0; i < workCount; i++) {
    const card = document.getElementById(`work-card-${i}`);
    if (!card) continue;
    const endVal = document.getElementById(`work-end-${i}`)?.value;
    workEntries.push({
      company: document.getElementById(`work-company-${i}`)?.value.trim() || "",
      designation: document.getElementById(`work-designation-${i}`)?.value.trim() || "",
      domain: document.getElementById(`work-domain-${i}`)?.value || "",
      employmentType: document.getElementById(`work-type-${i}`)?.value || "",
      startDate: document.getElementById(`work-start-${i}`)?.value || "",
      endDate: endVal || "Present",
      skills: (document.getElementById(`work-skills-${i}`)?.value || "").split(",").map(s => s.trim()).filter(Boolean),
    });
  }

  return { ...personal, educationPath: path, education, workExperience: workEntries };
}

// ============================================================
// SUBMIT FORM
// ============================================================
async function submitForm() {
  clearErrors();

  if (!selectedPath) {
    document.getElementById("err-path").textContent = "Please select an education path.";
    return;
  }

  const payload = collectFormData();

  // Show loading state
  document.getElementById("btn-text").style.display = "none";
  document.getElementById("btn-spinner").style.display = "inline";

  try {
    const response = await fetch(`${BACKEND_URL}/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok) {
      // Show field-level errors
      if (result.errors) {
        result.errors.forEach(err => {
          const el = document.getElementById(`err-${err.field}`);
          if (el) el.textContent = err.message;
        });
        showResult("rejected", null, result.errors);
      }
    } else {
      showResult("accepted", result);
    }

  } catch (err) {
    alert("Could not connect to backend. Please try again.");
    console.error(err);
  } finally {
    document.getElementById("btn-text").style.display = "inline";
    document.getElementById("btn-spinner").style.display = "none";
  }
}

// ============================================================
// SHOW RESULT
// ============================================================
function showResult(status, data, errors) {
  const screen = document.getElementById("result-screen");
  const title = document.getElementById("result-title");
  const body = document.getElementById("result-body");
  screen.style.display = "block";
  screen.scrollIntoView({ behavior: "smooth" });

  if (status === "rejected") {
    title.textContent = "❌ Application Rejected";
    title.style.color = "#e63946";
    body.innerHTML = `<p>Please fix the following errors and resubmit:</p>
      <ul class="flag-list">${errors.map(e => `<li>${e.message}</li>`).join("")}</ul>`;
    return;
  }

  const score = data.score;
  const colorClass = score >= 75 ? "score-green" : score >= 50 ? "score-yellow" : "score-red";
  const tagClass = score >= 75 ? "tag-green" : score >= 50 ? "tag-yellow" : "tag-red";

  title.textContent = "✅ Application Submitted Successfully!";
  title.style.color = "#2ecc71";

  body.innerHTML = `
    <div class="score-circle ${colorClass}">${score}</div>
    <p style="font-size:1.1rem; font-weight:600">Risk Score: ${score}/100</p>
    <span class="success-tag ${tagClass}">${data.category}</span>
    <p style="margin-top:10px; color:#666">Experience: ${data.experience_bucket}</p>
    ${data.flags && data.flags.length > 0 ? `
      <div class="flag-list">
        <strong>⚠️ Flags for Review:</strong>
        <ul>${data.flags.map(f => `<li>${f}</li>`).join("")}</ul>
      </div>` : `<p style="color:#2ecc71; margin-top:10px">✅ No flags — Clean Application</p>`}
    <p style="margin-top:15px; color:#888; font-size:0.85rem">Your application has been recorded in the system.</p>
  `;
}

function clearErrors() {
  document.querySelectorAll(".error").forEach(el => el.textContent = "");
}