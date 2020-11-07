<template>
    <div :class="classes">
        <slot></slot>
    </div>
</template>

<script>
export default {
    props: {
        span: {
            type: Number,
            default: 1
        }
    },
    computed: {
        classes: function() {
            let classes = {};
            classes["grid-col-" + this.span] = true;
            return classes;
        }
    }
}
</script>
