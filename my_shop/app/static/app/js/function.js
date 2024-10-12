var updateBtns = document.getElementsByClassName('update-cart')

for (i=0;i < updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId', productId, 'action',action)
    console.log('user : ', user)
    if (user === "AnonymousUser"){
        console.log('user not logged in')
    } else {
        updateUserOrder(productId,action)
    }
})}  

function updateUI(quantity) {
    const cartQuantityElement = document.getElementById('cart-quantity'); 
    if (cartQuantityElement) {
        cartQuantityElement.innerText = quantity; // Cập nhật số lượng hiển thị
    }
    console.log(`Updated cart quantity to: ${quantity}`);
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function updateUserOrder(productId, action, quantity) {
    var url = '/update_item/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,  
        },
        body: JSON.stringify({'productId': productId, 'action': action, 'quantity': quantity})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();  
    })
    .then(data => {
        console.log("Response data:", data); 
        if (data.message) {
            console.log(data.message);
            if (data.quantity !== undefined) {
                updateUI(data.quantity); 
            } else {
                console.error('Quantity not defined in response');
            }
            location.reload()
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}


