let adminChoiceContainerEl = document.getElementById("adminChoice");
let addMentorChoiceBtnEl = document.getElementById("addMentorChoiceBtn");

let addMentorFormContainerEl = document.getElementById("addMentorFormContainer");
let addMentorFormEl = document.getElementById("addMentorForm");


/* Upon Admin Choice for Adding Mentor to Intern*/

function displayAddMentorForm(resultObject) {

    let {interns_dict, mentors_dict} = resultObject

    let internSelectEl = document.getElementById("selectedInternForAddMentor");
    for (eachValue of Object.values(interns_dict)) {
        let internOptionEl = document.createElement("option");
        internOptionEl.textContent = eachValue;
        internSelectEl.appendChild(internOptionEl);
    }

    let mentorSelectEl = document.getElementById("selectedMentorForAddMentor");
    for (eachValue of Object.values(mentors_dict)) {
        let mentorOptionEl = document.createElement("option");
        mentorOptionEl.textContent = eachValue;
        mentorSelectEl.appendChild(mentorOptionEl);
    }
}

function getAddMentorFormData() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/interns-mentors");
    xhr.send();

    xhr.onreadystatechange = () => {
        /*console.log(typeof(xhr.response));*/

        if (xhr.readyState == 4 && xhr.status == 200) {
            resultObject = JSON.parse(xhr.response);
            console.log(resultObject)
            /* console.log(JSON.parse(xhr.response)); */
            displayAddMentorForm(resultObject);
        } else {
            console.log("Some error");
        }
    }
}

function uponAddMentorChoice() {
    adminChoiceContainerEl.classList.add("d-none");
    addMentorFormContainerEl.classList.remove("d-none");
    getAddMentorFormData();
}

addMentorChoiceBtnEl.addEventListener('click', uponAddMentorChoice);

/* Upon AddMentorForm Submit Button */

addMentorFormEl.addEventListener("submit", function(event) {
    event.preventDefault();
    console.log("Add Mentor Form Submitted");

    new FormData(addMentorFormEl);
});

addMentorFormEl.addEventListener("formdata", function(event) {
    console.log("formdata fired");

    let data = event.formData;
    let formObj = {};
    for (eachData of data) {
        formObj[eachData[0]] = eachData[1];
    }
    console.log(formObj);
    let xhr = new XMLHttpRequest();
    let stringifiedData = JSON.stringify(formObj);
    console.log(stringifiedData);
    xhr.open("POST", "/add-mentor");
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(stringifiedData);

    xhr.onreadystatechange = () => {
        /*console.log(typeof(xhr.response));*/

        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log("Successfully completed");
            console.log(xhr.responseText);
            msg=xhr.responseText
            displayOperationSuccess(msg);
        } else {
            console.log("Some error");
            displayOperationFailure("Please choose Intern and Mentor to proceed");
        }
    }
});

let statusMsgEl = document.getElementById("statusMsg");

function displayOperationSuccess(displayMsg) {
    statusMsgEl.textContent = displayMsg;
    statusMsgEl.classList.add("bg-success");
};

function displayOperationFailure(displayMsg) {
    statusMsgEl.textContent = displayMsg;
    statusMsgEl.classList.add("bg-danger");
};
