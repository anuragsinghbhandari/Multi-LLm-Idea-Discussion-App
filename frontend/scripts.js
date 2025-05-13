//to wake up backend//
fetch("https://discussion-pannel-ai.onrender.com/");
setTimeout(() => {
    window.scrollBy({ top: 250, behavior: "smooth" });
}, 7000);
/* Streaming Header test */
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

/* discussion start function after form submission */
document.getElementById('data-form').addEventListener("submit", async function(event){
    event.preventDefault();
    document.getElementById("right-container").innerHTML = "";
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

    const response = await fetch("https://discussion-pannel-ai.onrender.com/send_data/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    
    if (response.ok){
        if (window.eventSource){
            window.eventSource.close();
    
        };
        let msg =0;
        window.eventSource = new EventSource(`https://discussion-pannel-ai.onrender.com/discussion/`);
        
        window.eventSource.onmessage = function(event) {
            msg++;
            document.getElementById('right-container').innerHTML += event.data +"<br><br>";
            if (msg==15){
            window.eventSource.close();
            }
        };
        
        
        window.eventSource.onerror = function(event) {
            console.error("SSE Error:", event);
            window.eventSource.close();
        };
        console.log("last");
    };
   
});

document.getElementById('summarize').addEventListener("click", async function(event){
    event.preventDefault();
    const response = await fetch("https://discussion-pannel-ai.onrender.com/summarize/");
    if (response.ok){
        const data = await response.json();
        document.getElementById('right-container').innerHTML = 'Summary:\n' + data.summary;
    } else {
        console.log("Error getting summary")
    }
});
    