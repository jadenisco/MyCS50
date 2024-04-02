document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(null));

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email(email) {
  console.log("compose_email: " + email)

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (email == null) {
    // New Email
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    // Reply
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    if (email.subject.substr(0, 4) != 'RE: ') {
      document.querySelector('#compose-subject').value = 'RE: ' + `${email.subject}`;
    } else {
      document.querySelector('#compose-subject').value = `${email.subject}`;
    }

    replyBody = `\n\n>>>On ${email.timestamp} ${email.sender} wrote:\n`;
    email.body.split('\n').forEach((v) => {
      replyBody += '>>>' + v + '\n';
    });
    replyBody = replyBody.trimEnd();
    document.querySelector('#compose-body').value = replyBody;
  }
}


function renderEmailDetailView(email) {
  console.log("RenderEmailDetailView:" + email)

  contents = `
  <p><b>From: </b>${email.sender}</p>
  <p><b>To: </b>${email.recipients}</p>
  <p><b>Subject: </b>${email.subject}</p>
  <p><b>Timestamp: </b>${email.timestamp}</p>
  <button class="btn btn-sm btn-outline-primary" id="reply-button">Reply</button>
  <button class="btn btn-sm btn-outline-primary" id="archive-button">Archive</button>
  <button class="btn btn-sm btn-outline-primary" id="delete-button">Delete</button>
  <hr>
  <p style="white-space: pre-line">${email.body}</p>`;
  
  try {
    document.querySelector('.email-detail').innerHTML = contents;
  } catch (e) {
    const emailLink = document.createElement('div');
    emailLink.className = 'email-detail';
    emailLink.innerHTML = contents;
    document.querySelector('#email-details-view').append(emailLink);
  }

  document.querySelector('#reply-button').addEventListener('click', () => compose_email(email));
  document.querySelector('#archive-button').addEventListener('click', () => handleArchiveClick(email));
  document.querySelector('#delete-button').addEventListener('click', () => handleDeleteClick(email));
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'block';
}


function handleDeleteClick(email) {
  console.log("HandleDeleteClick: " + email.id);

  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({delete: true}),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  }).then((response) => {
    console.log("Response Status: ", response.status);
    load_mailbox('inbox');
  })
}
  
  
function handleArchiveClick(email) {
  console.log("HandleArchiveClick: " + email.id);
  
  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({archived: true}),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  }).then((response) => {
    console.log("Response Status: ", response.status);
    load_mailbox('inbox');
  })
}


function handleEmailClick(event) {
  console.log("HandleEmailClick");

  //Execute PUT using event.currentTarget.id
  fetch(`/emails/${event.currentTarget.id}`, {
    method: "PUT",
    body: JSON.stringify({read: true}),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })

  //Execute GET using event.currentTarget.id
  fetch(`/emails/${event.currentTarget.id}`)
  .then(response => response.json())
  .then(email => {
    if (email['error']) {
      console.error('Email was not found!')
    } else {
      console.log(email);
      renderEmailDetailView(email);
    }
  })
}


function renderEmailsView(mailbox, emails) {
  console.log("RenderEmailsView")

  emails.forEach((email, key) => {
    console.log("key: %s id: %s", key, email.id);

    if (email.read == true) {
      contents = `<div id="${email.id}" class="read-email" onclick="handleEmailClick(event)">`;
    } else {
      contents = `<div id="${email.id}" class="unread-email" onclick="handleEmailClick(event)">`;
    }
    contents += `
        <div><b>${email.sender}</b> ${email.subject}</div>
        <div class="timestamp">${email.timestamp}</div>
      </div>`;

    const emailLink = document.createElement('div')
    emailLink.className = 'email-link';
    emailLink.innerHTML = contents;
    document.querySelector('#emails-view').append(emailLink);
  })
}


function load_mailbox(mailbox) { 
  console.log("load_mailbox: %s", mailbox)

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    renderEmailsView(mailbox, emails)
  })
}


function post_form(event) {
  console.log("post_form event.target: " + event.target)

  const formData = new FormData(event.target);
  const data={}
  formData.forEach((value, key) => (data[key] = value))
  console.log(data);
  fetch("emails", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
  .then((response) => response.text())
  .then(text => console.log(text))
}
