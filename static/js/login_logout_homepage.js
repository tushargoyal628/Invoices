let no_of_clicks=1
function forgotpass() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const mobileno = document.getElementById("mobileno").value;
  
    if ((username && email &&no_of_clicks<2) || (username && mobileno &&no_of_clicks<2 ) || (email && mobileno &&no_of_clicks<2) || (email && mobileno && username &&no_of_clicks<2)) {
      no_of_clicks++;

      formdata={username:username,email:email,mobileno:mobileno};
      
      fetch('/handleforgotpass', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(formdata)
    })
    .then(response => response.json())
    .then(data=>{
        if(data.Status=="User Exists"){
            const newPasswordLabel = document.createElement("label");
            newPasswordLabel.textContent = "Enter New Password";
        
            const newPasswordInput = document.createElement("input");
            newPasswordInput.type = "password";
            newPasswordInput.id = "newPassword";
            newPasswordInput.required = true;

            const newwelcomelabel = document.createElement("label");
            newwelcomelabel.textContent = "Welcome "+data.NameOfUser;
            newwelcomelabel.style.color= "red";
            newwelcomelabel.style.textAlign= "center";

            const form = document.getElementById("search-form");
            const submitButton = document.getElementById("submit");
            const usernamelabel = document.getElementById("usernamelabel");
            form.insertBefore(newwelcomelabel,usernamelabel)
            form.insertBefore(newPasswordLabel, submitButton);
            form.insertBefore(newPasswordInput, submitButton);  
            document.getElementById("submit").textContent = "Change Password";
            document.getElementById("submit").onclick=changePassword;

        }
        else{
            alert(data.Status);
        }
    })

    } else {
        if(no_of_clicks>=2){
        alert("First change the password or go back")
    }else{
      alert("Please fill at least two of the three fields.");
    }
    }
  }


function changePassword() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const mobileno = document.getElementById("mobileno").value;
    const newPassword = document.getElementById("newPassword").value;
    formdata={Username:username,Email:email,Mobileno:mobileno,NewPassword:newPassword}

    if (newPassword) {
      
      fetch('/changepassword', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(formdata)
    })
    .then(response => response.json())
    .then(data=>{
        alert(data.Status)
    })

    } else {
      alert("Please enter a new password.");
    }
  }

function signUP(){
    const name=document.getElementById("name").value;
    const mobileno=document.getElementById("mobilenumber").value;
    const username=document.getElementById("username").value;
    const email=document.getElementById("email").value;
    const password=document.getElementById("password").value;
    
    const currentDateAndTime = new Date();

    const year = currentDateAndTime.getFullYear();
    const month = currentDateAndTime.getMonth() + 1;
    const day = currentDateAndTime.getDate();
    const hours = currentDateAndTime.getHours();
    const minutes = currentDateAndTime.getMinutes();
    const seconds = currentDateAndTime.getSeconds();  
    const formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

    if( name && mobileno && username && email && password ){
        formdata={
            name_of_user:name,
            mobileno:mobileno,
            username:username,
            emailid:email,
            password:password,
            accformdate:formattedDateTime
        }
        fetch('/handlesignup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify(formdata)
        })
        .then(response => response.json())
        .then(data => {
            if(data.Status=="User already exists"){
                const form = document.getElementById("search-form");
                const newInfoLabel = document.createElement("label");
                newInfoLabel.textContent = "User Already Exists. Kindly SignIn.Click Forgot Password If Forgotten Password ";
                const signupButton = document.getElementById("signup");
                form.insertBefore(newInfoLabel, signupButton);
                if(data.MatchingData=="Same MobileNo and Email Exists"){
                    alert("MobileNum "+mobileno+" And Email "+email+" Already Exists")
                }
                if(data.MatchingData=="Same MobileNo Exists"){
                    alert("MobileNum "+mobileno+" Already Exists")
                }
                if(data.MatchingData=="Same Email Exists"){
                    alert("Email "+email+" Already Exists")
                }
            }
            else{
                alert("New User Registered")
                document.getElementById("search-form").reset()
            }
        })
    }  
    else{
        alert("Kindly fill all the fields")
    }
     
}

function signIN(){
    const username=document.getElementById("username").value;
    const password=document.getElementById("password").value;
    const form = document.getElementById("search-form");
    
    formdata={username:username,password:password}
    
    if( username && password ){
        fetch('/handlesignin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify(formdata)
        })
        .then(response => response.json())
        .then(data => {
            if(data.Status=="User already exists"){
                alert("SignIn Successfull");
                form.reset()
                window.location.href="/main"
            }
            else{
                const newInfoLabel = document.createElement("label");
                newInfoLabel.textContent = "Either User Not Exist Or Check Username And Password ";
                const signupButton = document.getElementById("signin");
                form.insertBefore(newInfoLabel, signupButton);
            }
        })

    }  
    else{
        alert("Kindly fill all the fields")
    }
}


function returntoforgotpass(){
    window.location.href="/forgotpass"
}
function returntosignin(){
    window.location.href="/signin"
}
function returntosignup(){
    window.location.href="/signup"
}
function returntohomepage(){
    window.location.href="/"
}