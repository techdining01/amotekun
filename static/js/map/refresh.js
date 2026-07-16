class RefreshManager{

    constructor(){

        this.timers={};

    }

    start(){

        layerRegistry.all().forEach(layer=>{

            if(layer.refreshInterval){

                this.timers[layer.loader.name]=

                setInterval(

                    layer.loader,

                    layer.refreshInterval

                );

            }

        });

    }

    stop(){

        Object.values(this.timers)

            .forEach(clearInterval);

    }

}

window.refreshManager=new RefreshManager();