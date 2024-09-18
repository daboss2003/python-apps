document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox("inbox"));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox("sent"));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox("archive"));
  document.querySelector('#compose').addEventListener('click', compose_email);
  load_mailbox("inbox");
  // By default, load the inbox

  document.querySelector('#compose-form').addEventListener('submit',sendMail);
  let nav = document.getElementById("button");
  const openBtn = document.getElementById("open__btn");
  window.addEventListener("click", (e) => {
    if (e.target == openBtn){
      nav.style.display = "block";
    }
    else{
      nav.style.display = "none";
    }
    

  })

  // window.addEventListener("click", () =>{
  //   nav.style.display = "none";
  // })
  
});



function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#content-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}



function sendMail(){
  // Get values from the compose view
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;
  fetch('/emails',{
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => alert(result))
  .catch(error => alert('Error: ' + error)
  );
  load_mailbox("sent");
  

}



function load_mailbox(content){
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
  fetch(`/emails/${content}`)
  .then(response => response.json())
  .then(emails => {
    if(emails == ""){
      document.querySelector('#emails-view').innerHTML = `${content} Empty`;
    } else{
      displayResult(emails,content)
    }
  })
  .catch(error => console.error('Error',error))
}

function displayResult(result,content){
  let container = document.querySelector('#emails-view');
  container.innerHTML = "";
  container.className = "container text-center cc"
  let h1 = document.createElement('h1');
    h1.innerHTML = content;
    h1.className = "text-center text-primary center";
    container.appendChild(h1);
  result.forEach(result => {
    let inner_container = document.createElement('div');
    inner_container.className = "email-container";
    let p1 = document.createElement('p');
    p1.innerHTML = result.sender;
    p1.className = "sender"
    inner_container.appendChild(p1);
    let p2 = document.createElement('p');
    p2.innerHTML = result.subject;
    p2.className = "subject";
    inner_container.appendChild(p2);
    let p4 = document.createElement('p');
    p4.innerHTML = result.timestamp;
    p4.className = "timestamp";
    inner_container.appendChild(p4);
    if(result.read == true){
      inner_container.style.backgroundColor = "gray";
    } else{
      inner_container.style.backgroundColor = "white";
    }
    inner_container.addEventListener('click',() =>view_mail(result.id));
    container.appendChild(inner_container);
  });
}

function view_mail(email_id){
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => display_email(email))
  .catch(error => console.error(`Error${error}`))
}

function display_email(emails){
  const user_email = document.querySelector('#user_email').value;
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'block';
  let container = document.querySelector('#content-view');
  container.innerHTML = "";
  container.className = "container";
  if (emails.read != true){
    fetch(`/emails/${emails.id}`,{
      method: 'PUT',
      body: JSON.stringify({
        read:true
      })
    })
  }
  let inner_container = document.createElement('div');
    inner_container.className = "text-center cc";
    let h4 = document.createElement('h4');
    h4.innerHTML = emails.subject;
    h4.className = "text-center ";
    inner_container.appendChild(h4);
    let h5 = document.createElement('h5');
    h5.innerHTML = emails.sender;
    h5.className = "margin"
    inner_container.appendChild(h5);
    let p1 = document.createElement('p');
    p1.innerHTML = emails.timestamp;
    p1.className = "timestamp";
    inner_container.appendChild(p1);
    let p2 = document.createElement('p');
    p2.innerHTML = emails.body;
    p2.className = "email_body";
    inner_container.appendChild(p2);
    if(user_email != emails.sender){
      let button = document.createElement('button');
      button.className = "btn btn-primary m-3";
      if(emails.archived == true){
        button.innerHTML = "Unarchive"
        button.addEventListener('click',()=>{
          fetch(`/emails/${emails.id}`,{
            method:'PUT',
            body: JSON.stringify({
              archived:false
            })
          })
          load_mailbox("inbox");
        })
      } else{
        button.innerHTML = "Archive";
        button.addEventListener('click',()=>{
          fetch(`/emails/${emails.id}`,{
            method: 'PUT',
            body: JSON.stringify({
              archived:true
            })
          })
          load_mailbox("inbox");
        })

      }
      inner_container.appendChild(button);
      let reply_button = document.createElement('button');
      reply_button.innerHTML = "Reply";
      reply_button.className = "btn btn-primary m-3"
      reply_button.addEventListener('click',()=>reply_email(emails.sender,emails.subject,emails.body,emails.timestamp));
      inner_container.appendChild(reply_button);
    }
   
    container.appendChild(inner_container);
  
}


function reply_email(sender_email,subject,body,time){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#content-view').style.display = 'none';

  document.querySelector('#compose-recipients').value = sender_email;
  document.querySelector('#compose-subject').value = `Re:${subject}`;
  document.querySelector('#compose-body').value = `On ${time} ${sender_email} Wrote: ${body}`;
}
