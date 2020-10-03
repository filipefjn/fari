<template>
    <div>
        <!-- TODO -->
    </div>
</template>

<script>
export default {
    beforeMount: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "",
            subtitle: ""
        });
    },
    beforeDestroy: function() {
        //
    }

}
</script>
