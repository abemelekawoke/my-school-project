const button = document.querySelector('button');
button.addEventListener('click', (event) => {
    console.log(event);
})
function Events(params) {
    return <button onClick={(event) => console.log(event)}>Click</button>
}
