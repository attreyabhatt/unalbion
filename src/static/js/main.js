class AnimalArtifact {
    constructor(name = '', tier = '', price = '', empty = false) {

        if (price === "" || price == null) {
            empty = true
        } else {
            price = parseFloat(price);
            if (isNaN(price)) {
                throw new Error("Invalid price value");
            }
        }
        this.name = name;
        this.tier = tier;
        this.price = price;
        this.empty = empty;
    }
}

function isPositive(num) {
    if (num > 0) {
        return true;
    } else {
        return false;
    }
}

let t3shadow = new AnimalArtifact(
    document.getElementById("t3shadow").dataset.name,
    document.getElementById("t3shadow").dataset.tier,
    document.getElementById("t3shadow").value
);
let t5shadow = new AnimalArtifact(
    document.getElementById("t5shadow").dataset.name,
    document.getElementById("t5shadow").dataset.tier,
    document.getElementById("t5shadow").value
);
let t7shadow = new AnimalArtifact(
    document.getElementById("t7shadow").dataset.name,
    document.getElementById("t7shadow").dataset.tier,
    document.getElementById("t7shadow").value
);

let t3root = new AnimalArtifact(
    document.getElementById("t3root").dataset.name,
    document.getElementById("t3root").dataset.tier,
    document.getElementById("t3root").value
);
let t5root = new AnimalArtifact(
    document.getElementById("t5root").dataset.name,
    document.getElementById("t5root").dataset.tier,
    document.getElementById("t5root").value
);
let t7root = new AnimalArtifact(
    document.getElementById("t7root").dataset.name,
    document.getElementById("t7root").dataset.tier,
    document.getElementById("t7root").value
);

let t3spirit = new AnimalArtifact(
    document.getElementById("t3spirit").dataset.name,
    document.getElementById("t3spirit").dataset.tier,
    document.getElementById("t3spirit").value
);
let t5spirit = new AnimalArtifact(
    document.getElementById("t5spirit").dataset.name,
    document.getElementById("t5spirit").dataset.tier,
    document.getElementById("t5spirit").value
);
let t7spirit = new AnimalArtifact(
    document.getElementById("t7spirit").dataset.name,
    document.getElementById("t7spirit").dataset.tier,
    document.getElementById("t7spirit").value
);

let t3werewolf = new AnimalArtifact(
    document.getElementById("t3werewolf").dataset.name,
    document.getElementById("t3werewolf").dataset.tier,
    document.getElementById("t3werewolf").value
);
let t5werewolf = new AnimalArtifact(
    document.getElementById("t5werewolf").dataset.name,
    document.getElementById("t5werewolf").dataset.tier,
    document.getElementById("t5werewolf").value
);
let t7werewolf = new AnimalArtifact(
    document.getElementById("t7werewolf").dataset.name,
    document.getElementById("t7werewolf").dataset.tier,
    document.getElementById("t7werewolf").value
);

let t3imp = new AnimalArtifact(
    document.getElementById("t3imp").dataset.name,
    document.getElementById("t3imp").dataset.tier,
    document.getElementById("t3imp").value
);
let t5imp = new AnimalArtifact(
    document.getElementById("t5imp").dataset.name,
    document.getElementById("t5imp").dataset.tier,
    document.getElementById("t5imp").value
);
let t7imp = new AnimalArtifact(
    document.getElementById("t7imp").dataset.name,
    document.getElementById("t7imp").dataset.tier,
    document.getElementById("t7imp").value
);

let t3runestone = new AnimalArtifact(
    document.getElementById("t3runestone").dataset.name,
    document.getElementById("t3runestone").dataset.tier,
    document.getElementById("t3runestone").value
);
let t5runestone = new AnimalArtifact(
    document.getElementById("t5runestone").dataset.name,
    document.getElementById("t5runestone").dataset.tier,
    document.getElementById("t5runestone").value
);
let t7runestone = new AnimalArtifact(
    document.getElementById("t7runestone").dataset.name,
    document.getElementById("t7runestone").dataset.tier,
    document.getElementById("t7runestone").value
);

let t3dawn = new AnimalArtifact(
    document.getElementById("t3dawn").dataset.name,
    document.getElementById("t3dawn").dataset.tier,
    document.getElementById("t3dawn").value
);
let t5dawn = new AnimalArtifact(
    document.getElementById("t5dawn").dataset.name,
    document.getElementById("t5dawn").dataset.tier,
    document.getElementById("t5dawn").value
);

let t7dawn = new AnimalArtifact(
    document.getElementById("t7dawn").dataset.name,
    document.getElementById("t7dawn").dataset.tier,
    document.getElementById("t7dawn").value
);

function calcProfit(t3artifact, t5artifact, t7artifact, show_only_profit) {

    if (t3artifact.empty && !t5artifact.empty && !t7artifact.empty) {
        let profit75 = t5artifact.price - (t7artifact.price / 2);
        let profit_statement = "Profit from " + t7artifact.tier + " -> " + t5artifact.tier + " " + t3artifact.name + ": " + profit75;
        if (profit75 <= 0 && show_only_profit == true) {
            profit_statement = ''
        }
        return { profit75, profit_statement };
    } else if (t5artifact.empty && !t3artifact.empty && !t7artifact.empty) {
        let profit73 = t3artifact.price - (t7artifact.price / 4);
        let profit_statement = "Profit from " + t7artifact.tier + " -> " + t3artifact.tier + " " + t3artifact.name + ": " + profit73;
        if (profit73 <= 0 && show_only_profit == true) {
            profit_statement = ''
        }
        return { profit73, profit_statement };
    } else if (t7artifact.empty && !t3artifact.empty && !t5artifact.empty) {
        let profit53 = t3artifact.price - (t5artifact.price / 2);
        let profit_statement = "Profit from " + t5artifact.tier + " -> " + t3artifact.tier + " " + t3artifact.name + ": " + profit53;
        if (profit53 <= 0 && show_only_profit == true) {
            profit_statement = ''
        }
        return { profit53, profit_statement };
    } else if (!t3artifact.empty && !t5artifact.empty && !t7artifact.empty) {
        let profit75 = t5artifact.price - (t7artifact.price / 2);
        let profit73 = t3artifact.price - (t7artifact.price / 4);
        let profit53 = t3artifact.price - (t5artifact.price / 2);
        let profit_statement = t3artifact.name + ": " + t7artifact.tier + " -> " + t5artifact.tier + "= " + profit75 + "<br>"
            + t3artifact.name + ": " + t7artifact.tier + " -> " + t3artifact.tier + "= " + profit73 + "<br>"
            + t3artifact.name + ": " + t5artifact.tier + " -> " + t3artifact.tier + "= " + profit53 + "<br>";

        if (profit75 <= 0 && profit73 > 0 && profit53 > 0 && show_only_profit == true) {
            profit_statement = t3artifact.name + ": " + t7artifact.tier + " -> " + t3artifact.tier + "= " + profit73 + "<br>"
                + t3artifact.name + ": " + t5artifact.tier + " -> " + t3artifact.tier + "= " + profit53 + "<br>";
        }
        else if (profit53 <= 0 && profit75 > 0 && profit73 > 0 && show_only_profit == true) {
            profit_statement = t3artifact.name + ": " + t7artifact.tier + " -> " + t5artifact.tier + "= " + profit75 + "<br>"
                + t3artifact.name + ": " + t7artifact.tier + " -> " + t3artifact.tier + "= " + profit73 + "<br>";
        } else if (profit73 <= 0 && profit75 > 0 && profit53 > 0 && show_only_profit == true) {
            profit_statement = t3artifact.name + ": " + t7artifact.tier + " -> " + t5artifact.tier + "= " + profit75 + "<br>"
                + t3artifact.name + ": " + t5artifact.tier + " -> " + t3artifact.tier + "= " + profit53 + "<br>";
        } else if (profit75 <= 0 && profit73 <= 0 && profit53 <= 0 && show_only_profit == true) {
            profit_statement = '';
        } else if (profit75 <= 0 && profit73 <= 0 && profit53 > 0 && show_only_profit == true) {
            profit_statement = t3artifact.name + ": " + t5artifact.tier + " -> " + t3artifact.tier + "= " + profit53 + "<br>";
        } else if (profit75 <= 0 && profit73 > 0 && profit53 <= 0 && show_only_profit == true) {
            profit_statement = t3artifact.name + ": " + t7artifact.tier + " -> " + t3artifact.tier + "= " + profit73 + "<br>";
        } else if (profit75 > 0 && profit73 <= 0 && profit53 <= 0 && show_only_profit == true) {
            profit_statement = t3artifact.name + ": " + t7artifact.tier + " -> " + t5artifact.tier + "= " + profit75 + "<br>";
        }
        console.log(profit_statement)
        return { profit75, profit73, profit53, profit_statement };
    } else {
        profit_statement = t3artifact.name + "- Please fill in at least two artifact prices.<br>";
        return { profit_statement };
    }
}

document.getElementById("shadow_profit").innerHTML = calcProfit(t3shadow, t5shadow, t7shadow, true).profit_statement;
document.getElementById("root_profit").innerHTML = calcProfit(t3root, t5root, t7root, true).profit_statement;
document.getElementById("spirit_profit").innerHTML = calcProfit(t3spirit, t5spirit, t7spirit, true).profit_statement;
document.getElementById("werewolf_profit").innerHTML = calcProfit(t3werewolf, t5werewolf, t7werewolf, true).profit_statement;
document.getElementById("imp_profit").innerHTML = calcProfit(t3imp, t5imp, t7imp, true).profit_statement;
document.getElementById("runestone_profit").innerHTML = calcProfit(t3runestone, t5runestone, t7runestone, true).profit_statement;
document.getElementById("dawn_profit").innerHTML = calcProfit(t3dawn, t5dawn, t7dawn, true).profit_statement;

var checkbox = document.querySelector("input[name=show_only_profit]");

checkbox.addEventListener('change', function () {
    if (this.checked) {
        document.getElementById("shadow_profit").innerHTML = calcProfit(t3shadow, t5shadow, t7shadow, true).profit_statement;
        document.getElementById("root_profit").innerHTML = calcProfit(t3root, t5root, t7root, true).profit_statement;
        document.getElementById("spirit_profit").innerHTML = calcProfit(t3spirit, t5spirit, t7spirit, true).profit_statement;
        document.getElementById("werewolf_profit").innerHTML = calcProfit(t3werewolf, t5werewolf, t7werewolf, true).profit_statement;
        document.getElementById("imp_profit").innerHTML = calcProfit(t3imp, t5imp, t7imp, true).profit_statement;
        document.getElementById("runestone_profit").innerHTML = calcProfit(t3runestone, t5runestone, t7runestone, true).profit_statement;
        document.getElementById("dawn_profit").innerHTML = calcProfit(t3dawn, t5dawn, t7dawn, true).profit_statement;
    } else {
        document.getElementById("shadow_profit").innerHTML = calcProfit(t3shadow, t5shadow, t7shadow, false).profit_statement;
        document.getElementById("root_profit").innerHTML = calcProfit(t3root, t5root, t7root, false).profit_statement;
        document.getElementById("spirit_profit").innerHTML = calcProfit(t3spirit, t5spirit, t7spirit, false).profit_statement;
        document.getElementById("werewolf_profit").innerHTML = calcProfit(t3werewolf, t5werewolf, t7werewolf, false).profit_statement;
        document.getElementById("imp_profit").innerHTML = calcProfit(t3imp, t5imp, t7imp, false).profit_statement;
        document.getElementById("runestone_profit").innerHTML = calcProfit(t3runestone, t5runestone, t7runestone, false).profit_statement;
        document.getElementById("dawn_profit").innerHTML = calcProfit(t3dawn, t5dawn, t7dawn, false).profit_statement;
    }
});





document.getElementById("profit_row").classList.remove("d-none")