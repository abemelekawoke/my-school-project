(function () {
    "use strict";

    // Build fragment URL from the student id
    function fragmentUrl(studentId) {
        return "/admin/student/studentprofile/clearance-form/" + studentId + "/";
    }

    function closeModal() {
        const overlay = document.getElementById("clearanceModalOverlay");
        if (overlay) overlay.remove();
        // restore scrolling
        document.body.style.overflow = "";
    }

    function openModal(studentId) {
        closeModal(); // ensure single instance

        const overlay = document.createElement("div");
        overlay.id = "clearanceModalOverlay";
        overlay.innerHTML =
            '<div style="color:#fff;font-family:sans-serif;padding:20px;">Loading…</div>';
        document.body.appendChild(overlay);
        document.body.style.overflow = "hidden";

        fetch(fragmentUrl(studentId), {
            headers: { "X-Requested-With": "XMLHttpRequest" },
            credentials: "same-origin",
        })
            .then(function (r) {
                if (!r.ok) throw new Error("HTTP " + r.status);
                return r.text();
            })
            .then(function (html) {
                overlay.innerHTML = html;
                overlay.addEventListener("click", function (e) {
                    if (e.target === overlay) closeModal();
                });
            })
            .catch(function () {
                overlay.innerHTML =
                    '<div style="background:#fff;padding:20px;border-radius:8px;color:#b00020;">' +
                    "Failed to load clearance form.</div>";
            });
    }

    // ─── Global event delegation ─────────────────────────────
    document.addEventListener("click", function (e) {
        // Manual trigger: any element with [data-open-clearance]
        const trigger = e.target.closest("[data-open-clearance]");
        if (trigger) {
            e.preventDefault();
            openModal(trigger.getAttribute("data-student-id"));
            return;
        }
        // Close button
        if (e.target.closest("[data-modal-close]")) {
            e.preventDefault();
            closeModal();
        }
    });

    // ESC to close
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeModal();
    });

    // ─── Auto-open when action redirected with ?clearance_student=ID ─
    document.addEventListener("DOMContentLoaded", function () {
        const params = new URLSearchParams(window.location.search);
        const id = params.get("clearance_student");
        if (id) {
            // Strip the query param so refresh does not reopen
            window.history.replaceState({}, "", window.location.pathname);
            openModal(id);
        }
    });
})();