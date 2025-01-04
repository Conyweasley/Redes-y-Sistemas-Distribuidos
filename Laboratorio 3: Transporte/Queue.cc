#ifndef QUEUE
#define QUEUE

#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Queue: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
    int droppedPackages;
public:
    Queue();
    virtual ~Queue();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Queue);

Queue::Queue() {
    endServiceEvent = NULL;
}

Queue::~Queue() {
    cancelAndDelete(endServiceEvent);
}

void Queue::initialize() {
    buffer.setName("buffer");
    bufferSizeVector.setName("Paquetes en buffer");
    packetDropVector.setName("Paquetes eliminados");
    endServiceEvent = new cMessage("endService");
    droppedPackages = 0;
}

void Queue::finish() {
}

void Queue::handleMessage(cMessage *msg) {

    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // dequeue packet
            cPacket *pkt = (cPacket*) buffer.pop();
            bufferSizeVector.record(buffer.getLength());
            // send packet
            send(pkt, "out");
            // start new service
            simtime_t serviceTime = pkt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    } else { // if msg is a data packet

        //check  buffer limit
        if (buffer.getLength() >= par("bufferSize").intValue()){ //cambiado long por int
            //drop the packet
            delete msg;
            this->bubble("packet dropped");
            droppedPackages++;
            packetDropVector.record(droppedPackages); //1 o packetsdropped? revisar
        }
        else{
            //enqueue the packet
            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());
            //if the server is idle
            if (!endServiceEvent ->isScheduled()){
                //star the service
                scheduleAt(simTime(), endServiceEvent);
            }
        }
    }
}

#endif /* QUEUE */
