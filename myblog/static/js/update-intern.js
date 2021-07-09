/*
let adminChoiceUpdateInternContainerEl = document.getElementById("adminChoiceUpdateInternContainer");
let addMentorChoiceBtnEl = document.getElementById("addMentorChoiceBtn");

let addMentorFormContainerEl = document.getElementById("addMentorFormContainer");
let addMentorFormEl = document.getElementById("addMentorForm");


// Upon Admin Choice for Adding Mentor to Intern

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
        //console.log(typeof(xhr.response));

        if (xhr.readyState == 4 && xhr.status == 200) {
            resultObject = JSON.parse(xhr.response);
            console.log(resultObject)
            // console.log(JSON.parse(xhr.response));
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

// Upon AddMentorForm Submit Button

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
        //console.log(typeof(xhr.response));

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

*/
window.onload = function() {
    let adminChoiceUpdateInternContainerEl = document.getElementById("adminChoiceUpdateInternContainer");
    let assignMentorChoiceBtnEl = document.getElementById("assignMentorChoiceBtn");
    let assignMentorFormContainerEl = document.getElementById("assignMentorFormContainer");
    let assignMentorFormEl = document.getElementById("assignMentorForm");

    function displayAssignMentorFormData(response) {
        let { interns_dict, mentors_dict } = response;

        let internSelectEl = document.getElementById("selectedInternForAssignMentor");
        for (eachValue of Object.values(interns_dict)) {
            let internOptionEl = document.createElement("option");
            internOptionEl.textContent = eachValue;
            internSelectEl.appendChild(internOptionEl);
        }

        let mentorSelectEl = document.getElementById("selectedMentorForAssignMentor");
        for (eachValue of Object.values(mentors_dict)) {
            let mentorOptionEl = document.createElement("option");
            mentorOptionEl.textContent = eachValue;
            mentorSelectEl.appendChild(mentorOptionEl);
        }
    }

    function getAssignMentorFormData() {
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/interns-mentors');
        xhr.send();

        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4 && xhr.status == 200) {
                resultObject = JSON.parse(xhr.response);
                displayAssignMentorFormData(resultObject);
            }
        }
    }

    function onAssignMentor() {

        adminChoiceUpdateInternContainerEl.classList.add("d-none");
        assignMentorFormContainerEl.classList.remove("d-none");

        getAssignMentorFormData();
    }

    assignMentorChoiceBtnEl.addEventListener('click', onAssignMentor);

    assignMentorFormEl.addEventListener('submit', function(event){
        event.preventDefault();
        new FormData(assignMentorFormEl);
    });

    assignMentorFormEl.addEventListener('formdata', function(event){
        let data = event.formData;

        let formObj = {};
        for (eachData of data) {
            formObj[eachData[0]] = eachData[1];
        }

        let stringifiedData = JSON.stringify(formObj);

        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/assign-mentor");
        xhr.setRequestHeader("Content-type", "application/json");

        xhr.onreadystatechange = () => {

            if (xhr.readyState == 4 && xhr.status == 200) {
                msg=xhr.responseText;
                displayOperationSuccess(msg);
            } else if (xhr.status == 406) {
                msg=xhr.responseText;
                displayOperationFailure(msg);
            }
        }
        xhr.send(stringifiedData);
    });

    function displayOperationSuccess(message){
        let statusContainerEl = document.getElementById("operationStatusContainer");

        statusContainerEl.innerHTML = "";

        let msgContainerEl = document.createElement("div");
        msgContainerEl.classList.add("alert", "alert-success");
        msgContainerEl.role = "alert";
        msgContainerEl.textContent = message;
        statusContainerEl.appendChild(msgContainerEl);
    }

    function displayOperationInfo(message) {
        let statusContainerEl = document.getElementById("operationStatusContainer");

        statusContainerEl.innerHTML = "";

        let msgContainerEl = document.createElement("div");
        msgContainerEl.classList.add("alert", "alert-warning");
        msgContainerEl.role = "alert";
        msgContainerEl.textContent = message;
        statusContainerEl.appendChild(msgContainerEl);
    }

    function displayOperationFailure(message) {
        let statusContainerEl = document.getElementById("operationStatusContainer");

        statusContainerEl.innerHTML = "";

        let msgContainerEl = document.createElement("div");
        msgContainerEl.classList.add("alert", "alert-danger");
        msgContainerEl.role = "alert";
        msgContainerEl.textContent = message;
        statusContainerEl.appendChild(msgContainerEl);
    }



    // For deleting Assigned Mentor to an Intern

    let deleteAssignedMentorChoiceBtnEl = document.getElementById("deleteAssignedMentorChoiceBtn");
    let deleteAssignedMentorFormContainerEl = document.getElementById("deleteAssignedMentorFormContainer");

    let deleteAssignedMentorFormEl = document.getElementById("deleteAssignedMentorForm");

    let adminInputForDeletingAssignedMentorEl = document.getElementById("selectedInternForDeletingAssignedMentor");
    let mentorSelectionContainerForDeletingAssignedMentorEl = document.getElementById("mentorSelectionContainerForDeletingAssignedMentor");

    function getExistingInternsData() {
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/interns');
        xhr.send();

        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4 && xhr.status == 200) {
                resultObject = JSON.parse(xhr.response);
                availableInterns = Object.values(resultObject);
            }
        }
    }

    function onDeleteAssignedMentor() {
        adminChoiceUpdateInternContainerEl.classList.add("d-none");
        deleteAssignedMentorFormContainerEl.classList.remove("d-none");

        getExistingInternsData();
    }

    function onSuggestionSelection(event) {
        adminInputForDeletingAssignedMentorEl.value = event.target.textContent;
        let suggestionsContainerEl = document.getElementById("internSuggestionsContainerForDeletingAssignedMentor");
        suggestionsContainerEl.innerHTML = "";

        doNextForDeletingAssignedMentor();
    }

    function doNextForDeletingAssignedMentor() {
        if (mentorSelectionContainerForDeletingAssignedMentorEl.classList.contains("d-none") === false) {
            mentorSelectionContainerForDeletingAssignedMentorEl.classList.add("d-none");
        }

        let selectInternForDeletingAssignedMentorErrMsgEl = document.getElementById("selectInternForDeletingAssignedMentorErrMsg");
        let adminInputValue = adminInputForDeletingAssignedMentorEl.value;
        let isSelectionValid;
        if (adminInputValue !== "" && availableInterns.includes(adminInputValue)){
            selectInternForDeletingAssignedMentorErrMsgEl.textContent = "";
            isSelectionValid = true;
            mentorSelectionContainerForDeletingAssignedMentorEl.classList.remove("d-none");
        } else {
            selectInternForDeletingAssignedMentorErrMsgEl.textContent = "Please Input Valid Intern to proceed";
            selectInternForDeletingAssignedMentorErrMsgEl.style.color = "red";
            isSelectionValid = false;
        }

        if (isSelectionValid === true) {
            getCurrentMentorsForSelectedIntern(adminInputValue);
            let selectedMentorForDeletingAssignedMentorEl = document.getElementById("selectedMentorForDeletingAssignedMentor");
            selectedMentorForDeletingAssignedMentorEl.innerHTML = "";
        }
    }

    function getCurrentMentorsForSelectedIntern(selectedIntern) {
        let data = {"selectedIntern": selectedIntern };
        let stringifiedData = JSON.stringify(data);

        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/mentors-for-intern');
        xhr.setRequestHeader("Content-type", "application/json");

        xhr.onreadystatechange = () => {

            if (xhr.readyState == 4 && xhr.status == 200) {
                resultObject = JSON.parse(xhr.response);
                assignedMentors = Object.values(resultObject);
                displayCurrentAssignedMentors(assignedMentors);
            } else if (xhr.status == 406) {
                msg=xhr.responseText;
                displayOperationFailure(msg);
            }
        }
        xhr.send(stringifiedData);
    }

    function displayCurrentAssignedMentors(currentAssignedMentors) {
        let selectedMentorForDeletingAssignedMentorEl = document.getElementById("selectedMentorForDeletingAssignedMentor");
        for (eachExistingMentor of currentAssignedMentors) {
            let assignedMentorOptionEl = document.createElement("option");
            assignedMentorOptionEl.textContent = eachExistingMentor;
            selectedMentorForDeletingAssignedMentorEl.appendChild(assignedMentorOptionEl);
        }
    }

    function doSuggestInterns() {
        let inputValue = adminInputForDeletingAssignedMentorEl.value.toLowerCase();
        let suggestionsContainerEl = document.getElementById("internSuggestionsContainerForDeletingAssignedMentor");
        suggestionsContainerEl.innerHTML = "";
        if (inputValue !== "") {
            for (eachIntern of availableInterns) {
                if (eachIntern.toLowerCase().includes(inputValue)) {
                    let suggestionEl = document.createElement("li");
                    suggestionEl.style.listStyleType = "none";
                    suggestionEl.textContent = eachIntern;
                    suggestionEl.id = eachIntern;
                    suggestionEl.addEventListener('click', onSuggestionSelection);
                    suggestionsContainerEl.appendChild(suggestionEl);
                }
            }
        }
    }

    deleteAssignedMentorChoiceBtnEl.addEventListener('click', onDeleteAssignedMentor);

    adminInputForDeletingAssignedMentorEl.addEventListener('keyup', doSuggestInterns);

    adminInputForDeletingAssignedMentorEl.addEventListener('change', doNextForDeletingAssignedMentor);

    deleteAssignedMentorFormEl.addEventListener('submit', function(event){
        event.preventDefault();
        new FormData(deleteAssignedMentorFormEl);
    });

    deleteAssignedMentorFormEl.addEventListener('formdata', function(event){
        let data = event.formData;

        let formObj = {};
        for (eachData of data){
            formObj[eachData[0]] = eachData[1];
        }

        let stringifiedData = JSON.stringify(formObj);

        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/delete-assigned-mentor');
        xhr.setRequestHeader("Content-type", "application/json");

        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4 && xhr.status == 200) {
                msg=xhr.responseText;
                displayOperationSuccess(msg);
            } else if (xhr.status == 406) {
                msg=xhr.responseText;
                displayOperationFailure(msg);
            }
        }
        xhr.send(stringifiedData);
    });




    // For changing Intern Account Password



    let changeInternPasswordBtnEl = document.getElementById("changeInternPasswordBtn");
    let changeInternPasswordFormContainerEl = document.getElementById("changeInternPasswordFormContainer");

    let changeInternPasswordFormEl = document.getElementById("changeInternPasswordForm");

    let adminInputForChangingInternAccountPasswordEl = document.getElementById("selectedInternForChangingAccountPassword");
    let internAccountNewPasswordContainerForChangingInternAccountPasswordEl = document.getElementById("internAccountNewPasswordContainer");

    function onChangeInternPassword() {
        adminChoiceUpdateInternContainerEl.classList.add("d-none");
        changeInternPasswordFormContainerEl.classList.remove("d-none");

        getExistingInternsData();
    }

    function doSuggestInternsForChangeInternAccountPassword() {
        let inputValue = adminInputForChangingInternAccountPasswordEl.value.toLowerCase();
        let suggestionsContainerEl = document.getElementById("internSuggestionsContainerForChangingAccountPassword");
        suggestionsContainerEl.innerHTML = "";
        if (inputValue !== "") {
            for (eachIntern of availableInterns) {
                if (eachIntern.toLowerCase().includes(inputValue)) {
                    let suggestionEl = document.createElement("li");
                    suggestionEl.style.listStyleType = "none";
                    suggestionEl.textContent = eachIntern;
                    suggestionEl.id = eachIntern;
                    suggestionEl.addEventListener('click', onSuggestionSelectionForChangeInternAccountPassword);
                    suggestionsContainerEl.appendChild(suggestionEl);
                }
            }
        }
    }

    changeInternPasswordBtnEl.addEventListener('click', onChangeInternPassword);

    adminInputForChangingInternAccountPasswordEl.addEventListener('keyup', doSuggestInternsForChangeInternAccountPassword);

    adminInputForChangingInternAccountPasswordEl.addEventListener('change', doNextForChangeInternAccountPassword);

    function onSuggestionSelectionForChangeInternAccountPassword(event) {
        adminInputForChangingInternAccountPasswordEl.value = event.target.textContent;
        let suggestionsContainerEl = document.getElementById("internSuggestionsContainerForChangingAccountPassword");
        suggestionsContainerEl.innerHTML = "";

        doNextForChangeInternAccountPassword();
    }

    function doNextForChangeInternAccountPassword() {
        if (internAccountNewPasswordContainerForChangingInternAccountPasswordEl.classList.contains("d-none") == false) {
            internAccountNewPasswordContainerForChangingInternAccountPasswordEl.classList.add("d-none");
        }

        let selectInternForChangingAccountPasswordErrMsgEl = document.getElementById("selectInternForChangingAccountPasswordErrMsg");

        let adminInputValue = adminInputForChangingInternAccountPasswordEl.value;
        let isSelectionValid;
        if (adminInputValue !== "" && availableInterns.includes(adminInputValue)) {
            selectInternForChangingAccountPasswordErrMsgEl.textContent = "";
            isSelectionValid = true;
            internAccountNewPasswordContainerForChangingInternAccountPasswordEl.classList.remove("d-none");
        } else{
            selectInternForChangingAccountPasswordErrMsgEl.textContent = "Please Input Valid Intern to proceed";
            selectInternForChangingAccountPasswordErrMsgEl.style.color = "red";
            isSelectionValid = false;
        }

        if (isSelectionValid == true) {
            changeInternPasswordFormEl.addEventListener("submit", function(event){
                event.preventDefault();
                new FormData(changeInternPasswordFormEl);
            });
        }
    }

    changeInternPasswordFormEl.addEventListener('formdata', function(event){
        let data = event.formData;

        let formObj = {};
        for (eachData of data) {
            formObj[eachData[0]] = eachData[1];
        }

        let stringifiedData = JSON.stringify(formObj);

        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/change-intern-password');
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4 && xhr.status == 200) {
                msg = xhr.responseText;
                displayOperationSuccess(msg);
            } else {
                msg = xhr.responseText;
                displayOperationFailure(msg);
            }
        }
        xhr.send(stringifiedData);
    });


    // For Deleting Intern Account

    let deleteInternAccountChoiceBtnEl = document.getElementById("deleteInternAccountChoiceBtn");
    let deleteInternAccountFormContainerEl = document.getElementById("deleteInternAccountFormContainer");

    let deleteInternAccountFormEl = document.getElementById("deleteInternAccountForm");

    let adminInputForDeletingInternAccountEl = document.getElementById("selectedInternForDeletingInternAccount");
    let deleteInternAccountSubmitContainerEl = document.getElementById("deleteInternAccountSubmitContainer");

    function onDeleteInternAccount() {
        let msg = "Deleting Intern Account also deletes all his tasks and posts permanently";
        displayOperationInfo(msg);

        adminChoiceUpdateInternContainerEl.classList.add("d-none");
        deleteInternAccountFormContainerEl.classList.remove("d-none");

        getExistingInternsData();
    }

    function doSuggestInternsForDeleteInternAccount() {
        let inputValue = adminInputForDeletingInternAccountEl.value.toLowerCase();
        let suggestionsContainerEl = document.getElementById("internSuggestionsContainerForDeleteInternAccount");
        suggestionsContainerEl.innerHTML = "";
        if (inputValue !== "") {
            for (eachIntern of availableInterns) {
                if (eachIntern.toLowerCase().includes(inputValue)) {
                    let suggestionEl = document.createElement("li");
                    suggestionEl.style.listStyleType = "none";
                    suggestionEl.textContent = eachIntern;
                    suggestionEl.id = eachIntern;
                    suggestionEl.addEventListener('click', onSuggestionSelectionForDeleteInternAccount);
                    suggestionsContainerEl.appendChild(suggestionEl);
                }
            }
        }
    }


    deleteInternAccountChoiceBtnEl.addEventListener('click', onDeleteInternAccount);

    adminInputForDeletingInternAccountEl.addEventListener('keyup', doSuggestInternsForDeleteInternAccount);

    adminInputForDeletingInternAccountEl.addEventListener('change', doNextForDeleteInternAccount);

    function onSuggestionSelectionForDeleteInternAccount() {
        adminInputForDeletingInternAccountEl.value = event.target.textContent;
        let suggestionsContainerEl = document.getElementById("internSuggestionsContainerForDeleteInternAccount");
        suggestionsContainerEl.innerHTML = "";

        doNextForDeleteInternAccount();
    }

    function doNextForDeleteInternAccount() {
        if (deleteInternAccountSubmitContainerEl.classList.contains("d-none") == false) {
            deleteInternAccountSubmitContainerEl.classList.add("d-none");
        }

        let selectInternForDeleteInternAccountErrMsgEl = document.getElementById("selectInternForDeleteInternAccountErrMsg");

        let adminInputValue = adminInputForDeletingInternAccountEl.value;
        let isSelectionValid;
        if (adminInputValue !== "" && availableInterns.includes(adminInputValue)) {
            selectInternForDeleteInternAccountErrMsgEl.textContent = "";
            isSelectionValid = true;
            deleteInternAccountSubmitContainerEl.classList.remove("d-none");
        } else{
            selectInternForDeleteInternAccountErrMsgEl.textContent = "Please Input Valid Intern to proceed";
            selectInternForDeleteInternAccountErrMsgEl.style.color = "red";
            isSelectionValid = false;
        }

        if (isSelectionValid == true) {
            deleteInternAccountFormEl.addEventListener("submit", function(event){
                event.preventDefault();
                new FormData(deleteInternAccountFormEl);
            });
        }
    }

    deleteInternAccountFormEl.addEventListener("formdata", function(event) {
        let data = event.formData;

        let formObj = {};
        for (eachValue of data) {
            formObj[eachValue[0]] = eachValue[1];
        }

        let stringifiedData = JSON.stringify(formObj);

        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/delete-intern-account');
        xhr.setRequestHeader('Content-type', 'application/json');
        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4 && xhr.status == 200) {
                msg = xhr.responseText;
                displayOperationSuccess(msg);
            } else {
                msg = xhr.responseText;
                displayOperationFailure(msg);
            }
        }
        xhr.send(stringifiedData);
    });
}