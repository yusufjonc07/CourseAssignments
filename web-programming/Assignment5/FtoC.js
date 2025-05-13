// Converter function
function FtoCConverter(f){
    return (f - 32) * 5/9; // Calculation formula
}

// Handler function
function convertHandler(e){
    const f_input = document.getElementById("f_input").value  // Getting input value
    document.getElementById("c_result").innerText = FtoCConverter(f_input)  // Putting Calculation result
}