#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

#define NetSize 8

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    cStdDev hopStats;
    int array[NetSize];
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

static Packet* CreateHello(int source){
    //CreateHello crea un paquete setea el productor = consumidor, y la flag de IsHello en true.
    //El paquete tiene ByteLength = 1 para viajar lo mas rapido posible por la red.
    Packet *h = new Packet("hello");
    h->setByteLength(1);
    h->setSource(source);
    h->setDestination(source);
    h->setHopCount(1);
    h->setIsHello(true);
    h->setArray(source, -1);
    return h;

} 

void Net::initialize() {
    hopStats.setName("Total hops");
    //Creo 1 paquete Hello por cada nodo en la red.
    //Lo mando por el link 0 en sentido horario, recorre todos los nodos
    //y vuelve hacia su productor con un contador de cuantos saltos
    //le tomo al paquete llegar hasta cada nodo N.
    send(CreateHello(this->getParentModule()->getIndex()),"toLnk$o",0);
}

void Net::finish() {
    recordScalar("Average hops", hopStats.getMean());
    recordScalar("Max hops", hopStats.getMax());
}

void Net::handleMessage(cMessage *msg) {

    Packet *pkt = (Packet *) msg;
    //Caso el paquete es hello esto solo ocurre al inicio de la simulacion.
    if(pkt->isHello()){
        //EL paquete hello setea en su array interno cuantos saltos le tomo llegar hasta
        //el nodo actual y lo manda en sentido horario hacia el consumidor.
        if(pkt->getDestination() != this->getParentModule()->getIndex()){
            pkt->setArray(this->getParentModule()->getIndex(),pkt->getHopCount());
            pkt->setHopCount(pkt->getHopCount()+1);
            send(pkt,"toLnk$o",0);
        }
        //El nodo consumidor (que tambien es el productor) recibe el paquete hello, setea un array propio de cada
        //net con informacion de cual es el camino mas corto hasta cada nodo.
        //en este caso si la cantidad de saltos que le tomo llegar hasta N fue menor que la mitad del tamaño de Net
        //lo manda por sentido horario (Porque el paquete viajo en sentido horario y descubrio que era el mas optimo)
        //caso contrario lo setea en sentido antihorario.
        else{
            std::cout<<"Soy:"<<pkt->getSource()<<" ";
            for(size_t i=0; i<pkt->getArrayArraySize(); i++){
                if(pkt->getArray(i)<NetSize/2){
                    array[i] = 0;
                    std::cout<<"("<<i<<","<<"0) ";
                }
                else{
                    array[i] = 1;
                    std::cout<<"("<<i<<","<<"1) ";
                }
                
            }
            std::cout<<"\n";
            delete(pkt);
        }
    }
    //Caso el paquete no es hello, es decir el generado por la app.
    else{
        //Si el paquete se encuentra en el net productor, setea su direccion en setWay a la que
        //averiguo en el paso anterior de los paquetes hello y lo envia al siguiente.
        if(pkt->getSource()==this->getParentModule()->getIndex()){
            pkt->setWay(array[pkt->getDestination()]);
            pkt->setHopCount(pkt->getHopCount()+1);
            send(pkt,"toLnk$o",pkt->getWay());
        }
        //Si el paquete llego a destino es enviado a la aplicacion.
        else if(pkt->getDestination()==this->getParentModule()->getIndex()){
            pkt->setHopCount(pkt->getHopCount()+1);
            send(pkt,"toApp$o");
        }
        //Si el paquete esta en un nodo intermedio simplemente sigue su camino.
        else{
            pkt->setHopCount(pkt->getHopCount()+1);
            send(pkt,"toLnk$o",pkt->getWay());
        }
    }
}
