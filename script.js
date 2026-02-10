const API_URL = "http://127.0.0.1:8000";

function addEmployee() {
    const empId = document.getElementById("empId").value;
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const dept = document.getElementById("dept").value;

    if (!empId || !name || !email || !dept) {
        alert("Please fill all employee fields");
        return;
    }

    const data = {
        employeeId: parseInt(empId),
        fullName: name,
        email: email,
        department: dept
    };

    fetch(`${API_URL}/employees`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || data.error);
        getEmployees(); // refresh list
    })
    .catch(err => console.log(err));
}

// Get Employees
function getEmployees() {
    fetch(`${API_URL}/employees`)
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("employeeList");
        list.innerHTML = "";
        data.forEach(emp => {
            const li = document.createElement("li");
            li.textContent = `${emp.employeeId} - ${emp.fullName} (${emp.department})`;
            list.appendChild(li);
        });
    });
}

function markAttendance() {
    const empId = document.getElementById("attEmpId").value;
    const date = document.getElementById("attDate").value;
    const status = document.getElementById("status").value;

    if (!empId || !date || !status) {
        alert("Please fill all attendance fields");
        return;
    }

    const data = {
        employeeId: parseInt(empId),
        date: date,
        status: status
    };

    fetch(`${API_URL}/attendance`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => alert(data.message || data.error))
    .catch(err => console.log(err));
}
