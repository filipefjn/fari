<template>
    <button class="fari-button" v-bind="$attrs" v-on="listeners">
        <slot></slot>
    </button>
</template>

<script>
export default {
    inheritAttrs: false,
    computed: {
        listeners: function() {
            return Object.assign({}, this.$listeners);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.fari-button {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    margin: 0.5rem;
    padding: 0.75rem 1rem;
    background-color: #3E3E3E;
    // background-color: $primary;
    color: $text-color;
    // color: black;
    outline: none;
    border: none;
    box-shadow: $button-shadow;
    border-radius: 6px;
    font-size: 1rem;

    &:hover {
        background-color: #404040;
        // background-color: $primary-light;
    }

    &:active {
        box-shadow: $button-shadow-pressed;
        // background-color: #444444;
        // background-color: $primary-lighter;
        background-color: $primary;
        color: black;
    }

}

</style>
