function getCookie(name){
  let cookieValue = null;
  if(document.cookie && document.cookie !== ""){
    const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++){
        const cookie = cookies[i].trim();
        if (cookie.substring(0,name.length + 1) == (name + '=')){
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
  
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');





   

  function create_post(){
    if (document.querySelector('#post_submit_div').style.display == "none" && document.querySelector('#display_all_post').style.display == "block"){
      document.querySelector('#post_submit_div').style.display = "block";
      document.querySelector('#display_all_post').style.display = "none";
    } else{
      document.querySelector('#post_submit_div').style.display = "none";
      document.querySelector('#display_all_post').style.display = "block";
    }
  }

 

  function edit_post(){
      if (document.querySelector('#post_edit_div').style.display == "none" && document.querySelector('#display_post').style.display == "block"){
        document.querySelector('#post_edit_div').style.display = "block";
        document.querySelector('#display_post').style.display = "none";
      } else{
        document.querySelector('#post_edit_div').style.display = "none";
        document.querySelector('#display_post').style.display = "block";
      }
    }


  

  function open_friend(){
    const friend_container = document.querySelector('#friends_div')
    if (friend_container.style.display == "none"){
      friend_container.style.display = "block"
    } else{
      friend_container.style.display = "none"
    }
  }

  function view_note(note_id){
    fetch(`/get_notification`,{
      method: "PUT",
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({id: note_id })
    })
    .then(response => response.json())
    .then(result => console.log(JSON.stringify(result)))
    .catch(error => console.log('Error' + JSON.stringify(error)));
  }

  
document.addEventListener('DOMContentLoaded',()=>{
  const follow_button = document.querySelectorAll('.follow')
  follow_button.forEach(button =>{
    button.addEventListener('click',()=>{
      let user_id = button.dataset.id
      fetch(`/send_friend_request/${user_id}`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
      })
      .then(response => response.json())
      .then(data =>{
        if (data.response == "ok"){
          button.innerHTML = "Unfollow";
        } else{
          button.innerHTML = "Follow";
        }
      })
     
    })
  })




  document.body.addEventListener('click',(event)=>{
    let target = event.target
    if(target.classList.contains('like_buttons')){
      let post = target.closest('.max');
      if(post){
        let get_like = post.querySelector('.like_buttons');
        if (get_like){
    let post_id = get_like.dataset.post
    send_like(get_like,post_id)
  }
}
    }
  })
    
    

  document.body.addEventListener('click',(event)=>{
    let target = event.target
    if(target.classList.contains('comment_buttons')){
      let post = target.closest('.max');
      if(post){
        let comment_div = post.querySelector('.comment_div');
        if (comment_div){
          if(comment_div.style.display == "block"){
                     comment_div.style.display = "none"
                 } else{
                     comment_div.style.display = "block"
                }
        }
      }
    }
  })
 
})


async function send_like(get_like,post_id){
try{
  const response = await fetch(`/get_like/${post_id}`,{
   method: 'POST',
   headers: {
       'Content-Type': 'application/json',
       'X-CSRFToken': csrftoken,
   },
       body: JSON.stringify({ }),
  });

    if (!response.ok) {
       throw new Error(`Error:${response.status} - ${response.statusText}`);
    }
    const responseData = await response.json();
    console.log('Success',responseData);
    get_like.innerHTML = `${responseData.like_count} <i class="bi bi-hand-thumbs-up-fill"></i>`
    if(get_like.classList.contains('like')){
      get_like.classList.remove('like')
    } else{
      get_like.classList.add("like")
    }
    

} catch (error){
   console.error('Error:',error.message)
}
}