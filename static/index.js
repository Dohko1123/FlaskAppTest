// import axios from 'axios'
selectBox = "";

window.onload = function () {
    selectBox1 = document.getElementById("select1");
    selectBox2 = document.getElementById("select2");
    selectBox3 = document.getElementById("select3");
    selectBox4 = document.getElementById("select4");
}
function removeOptions() {
    var i, L = selectBox1.options.length - 1;
    for(i = L; i >= 0; i--) {
        selectBox1.remove(i);
        selectBox2.remove(i);
        selectBox3.remove(i);
        selectBox4.remove(i);
    }
    document.getElementById("graphicselect").style["display"] = "block";
    document.getElementById("graphicgenerate").style["display"] = "none";

    document.getElementById("column2").style["display"] = "none";
    document.getElementById("column3").style["display"] = "none";
    document.getElementById("column4").style["display"] = "none";
}

async function plotchart(id){
    removeOptions();
    document.getElementById("formtitle").textContent = document.getElementById(id).textContent;
    let response = await axios.get("/var_getter", {params: {"id": id}});
    if(response.status == 200){
        let required_columns = response.data.required;
        console.log(required_columns)
        let i = 1;
        while(i <= required_columns.length){
            document.getElementById(`column${i}`).style["display"] = "block";
            document.getElementById(`select${i}label`).textContent = required_columns[i-1];
            i++;
        };
        for(let i = 0; i < response.data.columns.length; i++){
            let option = response.data.columns[i];
            selectBox1.options.add(new Option(option, option));
            selectBox2.options.add(new Option(option, option));
            selectBox3.options.add(new Option(option, option));
            selectBox4.options.add(new Option(option, option));
        }
    }
    document.getElementById("graphicform").action = "/"+id;
    document.getElementById("graphicselect").style["display"] = "none";
    document.getElementById("graphicgenerate").style["display"] = "block";
}