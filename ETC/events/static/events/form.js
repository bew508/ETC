// On content loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create first performance div
    addPerformance()

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

    // Disable add rehearsal button if there are 10 elements
    if (rehearsals.children.length === 11)
        document.querySelector('form button#add-rehearsal-button').disabled = true

    // Enable remove rehearsal button
    document.querySelector('form button#remove-rehearsal-button').disabled = false

    return false
}

// Remove rehearsal button
function removeRehearsal() {
    // Delete latest rehearsal div
    const rehearsals = document.querySelector('div#rehearsals')
    rehearsals.removeChild(rehearsals.lastElementChild)

    // Enable add rehearsal button
    document.querySelector('form button#add-rehearsal-button').disabled = false

    // Disable remove rehearsal button if there are no elements remaining
    if (rehearsals.children.length === 1)
        document.querySelector('form button#remove-rehearsal-button').disabled = true
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

    // Disable add performance button if there are 10 elements
    if (performances.children.length === 11)
        document.querySelector('form button#add-performance-button').disabled = true

    // Enable remove performance button
    document.querySelector('form button#remove-performance-button').disabled = false

    return false
}

// Remove performance button
function removePerformance() {
    // Delete latest rehearsal div
    const performances = document.querySelector('div#performances')
    performances.removeChild(performances.lastElementChild)

    // Enable add rehearsal button
    document.querySelector('form button#add-performance-button').disabled = false

    // Disable remove performance button if there is one element remaining
    if (performances.children.length === 2)
        document.querySelector('form button#remove-performance-button').disabled = true

}