function calculateProfits() {
    let t3shadow_price = document.getElementById("t3shadow").value;
    let t5shadow_price = document.getElementById("t5shadow").value;
    let t7shadow_price = document.getElementById("t7shadow").value;

    // Function to check if a value is empty or contains only whitespace
    function isEmpty(value) {
        return value === null || value.trim() === "";
    }

    // Check if any input is empty
    if (isEmpty(t3shadow_price) || isEmpty(t5shadow_price) || isEmpty(t7shadow_price)) {
        console.log("Please fill in all input fields.");
        return;
    }

    // Convert input values to numbers
    t3shadow_price = parseFloat(t3shadow_price);
    t5shadow_price = parseFloat(t5shadow_price);
    t7shadow_price = parseFloat(t7shadow_price);

    // Check if conversion was successful
    if (isNaN(t3shadow_price) || isNaN(t5shadow_price) || isNaN(t7shadow_price)) {
        console.log("Please enter valid numeric values.");
        return;
    }

    // Calculate profits
    let profit = (t7shadow_price / 4) - t3shadow_price;
    let profit2 = (t5shadow_price / 2) - t3shadow_price;
    let profit3 = (t7shadow_price / 2) - t5shadow_price;

    console.log("Profit from T7:", profit);
    console.log("Profit from T5:", profit2);
     console.log("Profit from T5:", profit3);
}

calculateProfits();