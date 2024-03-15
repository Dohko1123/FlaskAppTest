// import axios from 'axios'
selectBox = "";

window.onload = function () {
    selectBox = document.getElementById("select");
}
function removeOptions() {
    var i, L = selectBox.options.length - 1;
    for(i = L; i >= 0; i--) {
        selectBox.remove(i);
    }
    document.getElementById("graphicselect").style["display"] = "block";
    document.getElementById("graphicgenerate").style["display"] = "none";
}

async function plotchart(id){
    removeOptions();
    document.getElementById("formtitle").textContent = document.getElementById(id).textContent;
    let response = await axios.get("/var_getter", {params: {"id": id}});
    if(response.status == 200){
        for(let i = 0; i < response.data.columns.length; i++){
            let option = response.data.columns[i];
            selectBox.options.add(new Option(option, option));
        }
    }
    document.getElementById("graphicform").action = "/"+id;
    document.getElementById("graphicselect").style["display"] = "none";
    document.getElementById("graphicgenerate").style["display"] = "block";
}