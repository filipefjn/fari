<template>
    <button class="np-list-row-button" v-bind="$attrs" v-on="$listeners">
        <slot></slot>
    </button>
</template>

<script>
export default {
    inheritAttrs: false
}
</script>
