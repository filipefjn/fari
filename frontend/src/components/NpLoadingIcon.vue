<template>
    <div class="np-loading-icon-wrapper">
        <img class="np-loading-icon" :style="styles" src="@/assets/loading-white.svg" v-on="$listeners"/>
    </div>
    
</template>

<script>
export default {
    props: {
        size: {
            type: String,
            default: "160px"
        }
    },
    computed: {
        styles: function() {
            let styles = {};
            if(this.size) {
                styles["height"] = this.size;
            }
            return styles;
        }
    }
}
</script>
