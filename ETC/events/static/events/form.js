// On content loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create first performance div
    console.log(document.querySelector('div#rehearsals').children.length)
    if (document.querySelector('div#rehearsals').children.length === 1)
        addPerformance()

    // Check on all buttons
    checkButtons()

    // Add onclick to add reahearsal button
    const addRehearsalButton = document.querySelector('form button#add-rehearsal-button')
    addRehearsalButton.onclick = addRehearsal

    // Add onclick to remove reahearsal button
    const removeRehearsalButton = document.querySelector('form button#remove-rehearsal-button')
    removeRehearsalButton.onclick = removeRehearsal

    // Add onlick to add performance button
    const addPerformanceButton = document.querySelector('form button#add-performance-button')
    addPerformanceButton.onclick = addPerformance

    // Add onlick to add performance button
    const removePerformanceButton = document.querySelector('form button#remove-performance-button')
    removePerformanceButton.onclick = removePerformance
})


// Add rehearsal button
function addRehearsal() {
    // Duplicate rehearsal section from template
    const rehearsals = document.querySelector('div#rehearsals')
    const rehearsalTemplate = document.querySelector('div#rehearsals template')
    let rehearsal = rehearsalTemplate.content.cloneNode(true)

    // Increment title, labels, and inputs
    rehearsal.querySelector('h5').innerHTML = `Rehearsal ${rehearsals.children.length}`

    rehearsals.append(rehearsal)

    checkButtons()

    return false
}

// Remove rehearsal button
function removeRehearsal() {
    // Delete latest rehearsal div
    const rehearsals = document.querySelector('div#rehearsals')
    rehearsals.removeChild(rehearsals.lastElementChild)

    checkButtons()

    return false
}

// Add performance button
function addPerformance() {
    // Duplicate performance section from template
    const performances = document.querySelector('div#performances')
    const performanceTemplate = document.querySelector('div#performances template')
    const performance = performanceTemplate.content.cloneNode(true)

    // Increment title, labels, and inputs
    performance.querySelector('h5').innerHTML = `Performance ${performances.children.length}`

    performances.append(performance)

    checkButtons()

    return false
}

// Remove performance button
function removePerformance() {
    // Delete latest rehearsal div
    const performances = document.querySelector('div#performances')
    performances.removeChild(performances.lastElementChild)

    checkButtons()

    return false
}

// Check the buttons
function checkButtons() {
    // Check rehearsal buttons
    const rehearsals = document.querySelector('div#rehearsals')

    // Add rehearsal button
    if (rehearsals.children.length >= 11)
        document.querySelector('form button#add-rehearsal-button').disabled = true
    else
        document.querySelector('form button#add-rehearsal-button').disabled = false

    // Remove rehearsal button
    if (rehearsals.children.length <= 1)
        document.querySelector('form button#remove-rehearsal-button').disabled = true
    else
        document.querySelector('form button#remove-rehearsal-button').disabled = false

    // Check performance buttons
    const performances = document.querySelector('div#performances')

    // Add performance button
    if (performances.children.length >= 11)
        document.querySelector('form button#add-performance-button').disabled = true
    else
        document.querySelector('form button#add-performance-button').disabled = false

    // Remove performance button
    if (performances.children.length <= 2)
        document.querySelector('form button#remove-performance-button').disabled = true
    else
        document.querySelector('form button#remove-performance-button').disabled = false
}