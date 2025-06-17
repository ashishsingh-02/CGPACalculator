let count = 0;

function addSubject() {
    count++;
    const div = document.createElement("div");
    div.innerHTML = `
        Subject ${count}: 
        <input type="text" placeholder="Grade (H/S/A/B/C/F/RA/K)" class="grade">
        <input type="number" placeholder="Credits" class="credit">
        <br>
    `;
    document.getElementById("inputs").appendChild(div);
}

function calculateCGPA() {
    const grades = document.querySelectorAll(".grade");
    const credits = document.querySelectorAll(".credit");

    let totalPoints = 0;
    let totalCredits = 0;
    const data = [];

    for (let i = 0; i < grades.length; i++) {
        const grade = grades[i].value.trim().toUpperCase();
        const credit = parseFloat(credits[i].value.trim());

        const gradeMap = { H: 10, S: 9, A: 8, B: 7, C: 6, F: 0, RA: 0, K: 0 };
        const point = gradeMap[grade];

        if (point === undefined || isNaN(credit)) {
            alert("Invalid input at subject " + (i + 1));
            return;
        }

        if (grade !== "RA" && grade !== "K") {
            totalPoints += point * credit;
            totalCredits += credit;
        }

        data.push({ grade, credit });
    }

    const cgpa = totalCredits ? (totalPoints / totalCredits).toFixed(2) : "N/A";
    document.getElementById("result").innerText = "CGPA: " + cgpa;

    // Send to server
    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subjects: data, cgpa })
    }).then(res => res.json()).then(msg => {
        console.log(msg);
    });
}
