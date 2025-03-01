setTimeout(() => {
    window.scrollBy({ top: 250, behavior: "smooth" });
}, 7000);

const paragraph = "Hi there, * We team of multiple llms are here to discuss your ideas, * ideas leads to greatness and let us help you give your ideas more perspectives.";
let index = 0;

function streamtext(){
    if (index<paragraph.length){
        if (paragraph[index]=='*'){
            document.getElementById("text-stream").innerHTML += '<br>';
        }
        else{
            document.getElementById("text-stream").innerHTML += paragraph[index];
        }
        
        index++;
        setTimeout(streamtext, 25);
    }
}

streamtext();
document.getElementById('data-form').addEventListener("submit", async function(event){
    event.preventDefault();
    const data = {
        topic: document.getElementById('topic').value,
        name: document.getElementById('name').value,
        name1: document.getElementById('name1').value,
        name2: document.getElementById('name2').value,
        name3: document.getElementById('name3').value,
        name4: document.getElementById('name4').value,
        profession: document.getElementById('profession').value,
        profession1:document.getElementById('profession1').value,
        profession2: document.getElementById('profession2').value,
        profession3: document.getElementById('profession3').value,
        profession4: document.getElementById('profession4').value,
    };
    
    const response = await fetch("http://127.0.0.1:8000/discussion/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    document.getElementById("right-container").innerHTML += result.message;
});


    
    