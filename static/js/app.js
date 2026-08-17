document.addEventListener("DOMContentLoaded", function () {

    // ================================
    // ADD TO CART
    // ================================

    document.querySelectorAll(".add-to-cart-btn").forEach(function (button) {

        button.addEventListener("click", async function () {

            if (button.dataset.loading === "true") {
                return;
            }

            const productId = button.dataset.productId;

            if (!productId) {
                console.error("Product ID missing");
                return;
            }

            const originalText = button.innerHTML;

            button.dataset.loading = "true";
            button.disabled = true;
            button.innerHTML = "⏳ Adding...";

            try {

                const response = await fetch(
                    "/cart/add/" + productId,
                    {
                        method: "POST",
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "Accept": "application/json"
                        }
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "Server returned " + response.status
                    );
                }

                const data = await response.json();

                console.log("Cart response:", data);

                if (data.login) {
                    window.location.href = "/";
                    return;
                }

                if (!data.ok) {
                    throw new Error(
                        data.message || "Could not add to cart"
                    );
                }

                const cartCount =
                    document.getElementById("cart-count");

                if (
                    cartCount &&
                    data.cart_count !== undefined
                ) {
                    cartCount.textContent = data.cart_count;
                }

                button.innerHTML = "✓ Added";
                button.classList.add("added");

                setTimeout(function () {

                    button.innerHTML = originalText;
                    button.classList.remove("added");
                    button.disabled = false;
                    button.dataset.loading = "false";

                }, 1000);

            } catch (error) {

                console.error("Cart Error:", error);

                button.innerHTML = "❌ Try Again";

                setTimeout(function () {

                    button.innerHTML = originalText;
                    button.disabled = false;
                    button.dataset.loading = "false";

                }, 1500);

            }

        });

    });


    // ================================
    // WISHLIST
    // ================================

    document.querySelectorAll(".heart").forEach(function (button) {

        button.addEventListener("click", async function () {

            if (button.dataset.loading === "true") {
                return;
            }

            const productId = button.dataset.product;

            if (!productId) {
                console.error("Wishlist product ID missing");
                return;
            }

            const symbol =
                button.querySelector(".heart-symbol");

            button.dataset.loading = "true";
            button.disabled = true;

            try {

                const response = await fetch(
                    "/wishlist/toggle/" + productId,
                    {
                        method: "POST",
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "Accept": "application/json"
                        }
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "Server returned " + response.status
                    );
                }

                const data = await response.json();

                console.log("Wishlist response:", data);

                if (data.login) {
                    window.location.href = "/";
                    return;
                }

                if (!data.ok) {
                    throw new Error(
                        data.message || "Wishlist error"
                    );
                }


                // ============================
                // ADDED TO WISHLIST
                // ============================

                if (data.active === true) {

                    button.classList.add("active");

                    if (symbol) {
                        symbol.textContent = "♥";
                    }

                    button.setAttribute(
                        "title",
                        "Remove from Wishlist"
                    );

                    button.setAttribute(
                        "aria-label",
                        "Remove from Wishlist"
                    );

                }


                // ============================
                // REMOVED FROM WISHLIST
                // ============================

                else {

                    button.classList.remove("active");

                    if (symbol) {
                        symbol.textContent = "♡";
                    }

                    button.setAttribute(
                        "title",
                        "Add to Wishlist"
                    );

                    button.setAttribute(
                        "aria-label",
                        "Add to Wishlist"
                    );

                }


                // ============================
                // UPDATE WISHLIST COUNT
                // ============================

                const wishlistCount =
                    document.getElementById("wishlist-count");

                if (
                    wishlistCount &&
                    data.wishlist_count !== undefined
                ) {
                    wishlistCount.textContent =
                        data.wishlist_count;
                }

            } catch (error) {

                console.error(
                    "Wishlist Error:",
                    error
                );

            } finally {

                button.disabled = false;
                button.dataset.loading = "false";

            }

        });

    });


    // ================================
    // FORM BUTTON LOCK
    // ================================

    document.querySelectorAll("form").forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButton =
                form.querySelector(
                    "button[type='submit']"
                );

            if (!submitButton) {
                return;
            }

            if (submitButton.dataset.lock === "true") {
                return;
            }

            setTimeout(function () {

                submitButton.disabled = true;
                submitButton.dataset.lock = "true";

            }, 0);

        });

    });


    // ================================
    // FLASH MESSAGE AUTO HIDE
    // ================================

    setTimeout(function () {

        document.querySelectorAll(".flash").forEach(function (message) {

            message.style.opacity = "0";
            message.style.transition = "opacity 0.4s";

            setTimeout(function () {

                message.remove();

            }, 400);

        });

    }, 3000);

});