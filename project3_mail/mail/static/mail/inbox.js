document.addEventListener('DOMContentLoaded', function() {

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
	document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
	document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
	document.querySelector('#compose').addEventListener('click', compose_email);
	document.querySelector('#compose-form').addEventListener('submit', send_email);

	// By default, load the inbox
	load_mailbox('inbox');
});

function send_reply(emailId) {
	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';

	// Prefill composition fields with email contents
	fetch(`emails/${emailId}`)
	.then(response => response.json())
	.then(email => {
		document.querySelector('#compose-recipients').value = `${email.sender}`;
		document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
		document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:${email.body}`
	});
}

function get_email(event) {
	console.log('Reached!');

	// Show email view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'block';
	document.querySelector('#compose-view').style.display = 'none';

	// Obtain the id attribute to fetch the email object
	emailId = parseInt(event.target.getAttribute('id'));

	// Track if the email is in the 'Sent' folder
	isSent = event.target.getAttribute('sent');

	document.querySelector('.reply').addEventListener('click', send_reply.bind(this, emailId));

	fetch(`emails/${emailId}`)
	.then(response => response.json())
	.then(email => {
		// Show the email contents
		document.querySelector('.timestamp').innerHTML = `Sent: ${email.timestamp}`;
		document.querySelector('.sender').innerHTML = `From: ${email.sender}`;
		document.querySelector('.recipients').innerHTML = `To: ${email.recipients}`;
		document.querySelector('.subject').innerHTML = `Subject: ${email.subject}`;
		document.querySelector('.body').innerHTML = `${email.body}`;

		// Show an archive/unarchive button depending on the email's state
		let archive = document.querySelector('.archive');
		if (isSent === 'false') {
			document.querySelector('.archive').style.display = 'block';
			if (email.archived) {
			archive.innerHTML = `Unarchive`;
			} else {
				archive.innerHTML = `Archive`;
			}
		} else {
			archive.style.display = 'none';
		}

		// Send a PUT request toggling the archive state of the email if clicked
		archive.addEventListener('click', () => {
			isArchived = archive.innerHTML === 'Unarchive';
			fetch(`emails/${emailId}`, {
				method: 'PUT',
				body: JSON.stringify({
					archived: !isArchived
				})
			})
			// Wait for the fetch request before loading the inbox
			setTimeout(function(){load_mailbox('inbox');}, 1000);
		})
	});

	// Mark the email as read when opened
	fetch(`emails/${emailId}`, {
		method: 'PUT',
		body: JSON.stringify({
			read: true
		})
	})
}

function send_email(event) {
	event.preventDefault();
	console.log("Hey!");
	fetch('/emails', {
		method: 'POST',
		body: JSON.stringify({
			recipients: document.querySelector('#compose-recipients').value,
			subject: document.querySelector('#compose-subject').value,
			body: document.querySelector('#compose-body').value
		})
	})
	.then(response => response.json())
	.then(result => {
		if (result.message != undefined) {
			load_mailbox('sent');
			console.log(result);
		} else {
			console.log(result.error);
		}
	});
}

function compose_email() {

	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';

	// Clear out composition fields
	document.querySelector('#compose-recipients').value = '';
	document.querySelector('#compose-subject').value = '';
	document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'none';

	// Show the mailbox name
	document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

	fetch(`/emails/${mailbox}`)
	.then(response => response.json())
	.then(emails => {
		emails.forEach(email => {
			mailboxContainer = document.querySelector('#emails-view');

			emailContainer = document.createElement('div');
			emailContainer.classList.add('email-container');
			emailContainer.setAttribute('id', `${email.id}`);
			if (mailbox === 'sent') {
				emailContainer.setAttribute('sent', `true`);
			} else {
				emailContainer.setAttribute('sent', `false`);
			}
			emailContainer.addEventListener('click', get_email);
			mailboxContainer.append(emailContainer);

			content = document.createElement('div');
			timestamp = document.createElement('div');
			emailContainer.append(content, timestamp);

			content.innerHTML = `<h3>${email.subject}</h3><p>${email.sender}</p>`
			timestamp.innerHTML = `<p>${email.timestamp}</p>`
		});
	});
}