---
asset_id: 28AEDF62F12B289C88BD6659BD6E50CC
author: Kleppmann Martin
modified_date: '2024-01-17T21:04:52'
title: Designing DataIntensive Applications
---

# Designing DataIntensive Applications

By Kleppmann Martin

## My notes <a name="my_notes_dont_delete"></a>



## iBooks notes <a name="ibooks_notes_dont_delete"></a>

The things that can go wrong are called faults, and systems that anticipate faults and can cope
with them are called fault-tolerant or resilient

It is impossible to reduce the probability of a fault to zero;
therefore it is usually best to design fault-tolerance mechanisms that prevent faults from causing
failures

Even in “noncritical” applications we have a responsibility to our users

when developing a prototype product for an unproven market

One common reason for degradation is increased load

Scalability is the term we use to describe a system’s ability to cope with increased load

This works better because the average
rate of published tweets is almost two orders of magnitude lower than the rate of home timeline
reads, and so in this case it’s preferable to do more work at write time and less at read time.

The final twist of the Twitter anecdote: now that approach 2 is robustly implemented, Twitter is
moving to a hybrid of both approaches. Most users’ tweets continue to be fanned out to home
timelines at the time when they are posted, but a small number of users with a very large number of
followers (i.e., celebrities) are excepted from this fan-out

Usually it is better to use percentiles. If you take your list of response times and sort it from
fastest to slowest, then the median is the halfway point

This makes the median a good metric if you want to know how long users typically have to wait: half
of user requests are served in less than the median response time, and the other half take longer
than the median  _NOTE: P50_

In order to figure out how bad your outliers are, you can look at higher percentiles: the 95th,
99th, and 99.9th percentiles are common (abbreviated p95, p99, and p999). They are the
response time thresholds at which 95%, 99%, or 99.9% of requests are faster than that particular
threshold. For example, if the 95th percentile response time is 1.5 seconds, that means 95 out of
100 requests take less than 1.5 seconds, and 5 out of 100 requests take 1.5 seconds or more. This is
illustrated in Figure 1-4.





When generating load artificially in order to test the scalability of a system, the load-generating
client needs to keep sending requests independently of the response time. If the client waits for
the previous request to complete before sending the next one, that behavior has the effect of
artificially keeping the queues shorter in the test than they would be in reality, which skews the
measurements

While distributing stateless services across multiple machines is fairly straightforward, taking
stateful data systems from a single node to a distributed setup can introduce a lot of additional
complexity. For this reason, common wisdom until recently was to keep your database on a single
node (scale up) until scaling cost or high-availability requirements forced you to make it
distributed

In an early-stage startup or an unproven product it’s usually more important to
be able to iterate quickly on product features than it is to scale to some hypothetical future
load.

Operability

Simplicity

Evolvability

A software
project mired in complexity is sometimes described as a big ball of mud
[30].

Making a system simpler does not necessarily mean reducing its functionality; it can also mean
removing accidental complexity. Moseley and Marks
[32] define complexity as accidental if
it is not inherent in the problem that the software solves (as seen by the users) but arises only
from the implementation

One of the best tools we have for removing accidental complexity is abstraction. A good
abstraction can hide a great deal of implementation detail behind a clean, simple-to-understand
façade

data is organized into relations (called tables in SQL), where each relation is an unordered collection
of tuples (rows in SQL).

greater scalability than relational databases

Specialized query operations that are not well supported by the relational model  _NOTE: Joins _

more dynamic and
expressive data model 

If the database itself does not support joins, you have to emulate a join in application code by
making multiple queries to the database

Document databases reverted back to the hierarchical model in one aspect: storing nested records

The main arguments in favor of the document data model are schema flexibility, better performance
due to locality, and that for some applications it is closer to the data structures used by the
application  _NOTE: But no querying by filtering the nested structure _

If the data in your application has a document-like structure (i.e., a tree of one-to-many
relationships, where typically the entire tree is loaded at once), then it’s probably a good idea to
use a document model  _NOTE: Without having to demoralize the data later in rdms, u can use document db _

you cannot refer directly to a nested item  _NOTE: Cannot directly extra position of an employee. Need to go through the hierarchy until u reach the position node, so to speak _

Joins can be emulated in
application code by making multiple requests to the database, but that also moves complexity into
the application and is usually slower than a join performed by specialized code inside the
database

there is an implicit schema, but it is not
enforced by the database

There are many different types of objects, and it is not practical to put each type of object in
its own table.


The structure of the data is determined by external systems over which you have no control and
which may change at any time.

But in cases where all records are expected to have the same
structure, schemas are a useful mechanism for documenting and enforcing that structure

The
database typically needs to load the entire document, even if you access only a small portion of it,
which can be wasteful on large documents  _NOTE: Demerits of doc model_

SQL is a
declarative query language  _NOTE: U tell it what u want.. not how to_

is up to the database
system’s query optimizer to decide which indexes and which join methods to use, and in which order
to execute various parts of the query.

Imperative code is very hard to parallelize across multiple cores and multiple machines, because it
specifies instructions that must be performed in a particular order. Declarative languages have a
better chance of getting faster in parallel execution because they specify only the pattern of the
results, not the algorithm that is used to determine the results. The database is free to use a
parallel implementation of the query language, if appropriate

This is easy, using CSS  _NOTE: CSS is declarative_

In a web browser, using declarative CSS styling is much better than manipulating styles imperatively in
JavaScript. Similarly, in databases, declarative query languages like SQL turned out to be much
better than imperative query APIs

MapReduce is a programming model for processing large amounts of data in bulk across many
machines

map (also known as collect) and reduce (also
known as fold or inject

The map and reduce functions are somewhat restricted in what they are allowed to do. They must be
pure functions, which means they only use the data that is passed to them as input, they cannot
perform additional database queries

If your application has mostly one-to-many relationships (tree-structured
data) or no relationships between records, the document model is appropriate.

But what if many-to-many relationships are very common in your data? The relational model can handle
simple cases of many-to-many relationships, but as the connections within your data become more
complex, it becomes more natural to start modeling your data as a graph.

maelstrom  _NOTE: A huge number of (whirlpool)_

plethora  _NOTE: A huge number of ; excess of_

hubris  _NOTE: Excess pride ; ghamand_

Historically, data started out being represented as one big tree (the hierarchical model), but that
wasn’t good for representing many-to-many relationships, so the relational model was invented to
solve that problem. More recently, developers found that some applications don’t fit well in the
relational model either. New nonrelational “NoSQL” datastores have diverged in two main
directions:


Document databases target use cases where data comes in self-contained documents and
relationships between one document and another are rare.


Graph databases go in the opposite direction, targeting use cases where anything is potentially
related to everything.

One thing that document and graph databases have in common is that they typically don’t enforce a
schema for the data they store, which can make it easier to adapt applications to changing
requirements

Similarly to what db_set does, many databases
internally use a log, which is an append-only data file

Any kind of index usually slows down writes, because the index also needs
to be updated every time data is written.

This is an important trade-off in storage systems: well-chosen indexes speed up read queries, but
every index slows down writes. For this reason, databases don’t usually index everything by default,
but require you—the application developer or database administrator—to choose indexes
manually, using your knowledge of the application’s typical query patterns

Compaction
means throwing away duplicate keys in the log, and keeping only the most recent update for each key.




Range queries are not efficient

one key for every few kilobytes of segment file is sufficient

There are plenty of well-known tree data structures that you can use, such
as red-black trees or AVL trees [2]. With
these data structures, you can insert keys in any order and read them back in sorted order.

LSM-trees, which only append to files (and eventually delete obsolete files)

B-tree implementations to
include an additional data structure on disk: a write-ahead log (WAL, also known as a redo log).
This is an append-only file to which every B-tree modification must be written before it can be
applied to the pages of the tree itself

LSM-trees are typically faster for writes, whereas B-trees are thought to be faster for reads


A B-tree index must write every piece of data at least twice: once to the write-ahead log, and once
to the tree page itself

There is also overhead from having
to write an entire page at a time, even if only a few bytes in that page changed

Moreover, LSM-trees are typically able to sustain higher write throughput than

B-trees, partly because they
sometimes have lower write amplification  _NOTE: Consequent writes from writes growing over time_

downside of log-structured storage is that the compaction process can sometimes interfere with the
performance of ongoing reads and writes.

but the bigger the database gets, the more disk
bandwidth is required for compaction.

you can create several
secondary indexes on the same table using the CREATE INDEX command, and they are often crucial
for performing joins efficiently.

each index just references a location
in the heap file, and the actual data is kept in one place.

The situation is more complicated if the new value is larger, as it probably needs to be moved to a
new location in the heap where there is enough space. In that case, either all indexes need to be
updated to point at the new heap location of the record, or a forwarding pointer is left behind in
the old heap location

A compromise between a clustered index (storing all row data within the index) and a nonclustered
index (storing only references to the data within the index

Some in-memory key-value stores, such as Memcached, are intended for caching use only, where it’s
acceptable for data to be lost if a machine is restarted

Table 3-1. Comparing characteristics of transaction processing versus analytic systems

OLTP systems for analytics purposes, and to run the analytics on a separate
database instead. This separate database was called a data warehouse.

They are usually reluctant to let business analysts
run ad hoc analytic queries on an OLTP database

A data warehouse, by contrast, is a separate database that analysts can query to their hearts’
content, without affecting OLTP operations
[48].
The data warehouse contains a read-only copy of the data in all the various OLTP systems in the
company. Data is extracted from OLTP databases (using either a periodic data dump or a continuous
stream of updates), transformed into an analysis-friendly schema, cleaned up, and then loaded into
the data warehouse. This process of getting data into the warehouse is known as
Extract–Transform–Load (ETL

It turns out
that the indexing algorithms discussed in the first half of this chapter work well for OLTP, but are
not very good at answering analytic queries

The data model of a data warehouse is most commonly relational, because SQL is generally a good fit
for analytic queries

Many data warehouses are used in a fairly formulaic
style, known as a star schema  _NOTE: Fact table in middle with dimension tables as rays of a star_

Analyzing whether people are more inclined to buy fresh fruit or candy, depending on the day of the week  _NOTE: Example analytics query_

The idea behind column-oriented storage is simple: don’t store all the values from one row
together, but store all the values from each column together instead. 

The column-oriented storage layout relies on each column file containing the rows in the same order.
Thus, if you need to reassemble an entire row, you can take the 23rd entry from each of the
individual column files and put them together to form the 23rd row of the table.

However, they have the downside of making writes more difficult.

An update-in-place approach, like B-trees use, is not possible with compressed columns. If you
wanted to insert a row in the middle of a sorted table, you would most likely have to rewrite all
the column files. As rows are identified by their position within a column, the insertion has to
update all columns consistently.

LSM-trees. All writes
first go to an in-memory store, where they are added to a sorted structure and prepared for writing
to disk. It doesn’t matter whether the in-memory store is row-oriented or column-oriented. When
enough writes have accumulated, they are merged with the column files on disk and written to new
files in bulk

One way of creating such a cache is a materialized view. In a relational data model, it is often
defined like a standard (virtual) view: a table-like object whose contents are the results of some
query

When the underlying data changes, a materialized view needs to be updated, because it is a
denormalized copy of the data. The database can do that automatically, but such updates make writes
more expensive, which is why materialized views are not often used in OLTP databases. In read-heavy
data warehouses they can make more sense

A common special case of a materialized view is known as a data cube or OLAP cube

OLTP systems are typically user-facing, which means that they may see a huge volume of requests

The application requests records using some kind of key, and the storage engine uses an
index to find the data for the requested key. Disk seek time is often the bottleneck here.

but each query is typically very demanding, requiring many millions of records to be
scanned in a short time

When you want to write data to a file or send it over the network, you have to encode it as some
kind of self-contained sequence of bytes

Many programming languages come with built-in support for encoding in-memory objects into byte
sequences. For example, Java has java.io.Serializable
[1], Ruby has Marshal
[2], Python has pickle
[3],
and so on

The encoding is often tied to a particular programming language

the decoding process needs to be able to
instantiate arbitrary classes

they often neglect the inconvenient problems of forward and backward
compatibility.

There is a lot of ambiguity around the encoding of numbers

JSON distinguishes strings and numbers, but it doesn’t distinguish integers and
floating-point numbers

Unicode character strings (i.e., human-readable text

but they
don’t support binary strings (sequences of bytes without a character encoding). Binary strings are a
useful feature, so people get around this limitation by encoding the binary data as text using
Base64

use a lot of space

profusion  _NOTE: Plethora_

Both Thrift and Protocol Buffers require a schema for any data that is encoded

Thrift has a dedicated list datatype, which is parameterized with the datatype of the list
elements. This does not allow the same evolution from single-valued to multi-valued as Protocol
Buffers does, but it has the advantage of supporting nested lists.

First of all, notice that there are no tag numbers in the schema. If we encode our example record
(Example 4-1) using this schema, the Avro binary encoding is just 32 bytes long—the
most compact of all the encodings we have seen

To parse the binary data, you go through the fields in the order that they appear in the schema and
use the schema to tell you the datatype of each field. This means that the binary data can only be
decoded correctly if the code reading the data is using the exact same schema as the code that
wrote the data. Any mismatch in the schema between the reader and the writer would mean incorrectly
decoded data.

The key idea with Avro is that the writer’s schema and the reader’s schema don’t have to be the
same—they only need to be compatible. When data is decoded (read), the Avro library resolves the
differences by looking at the writer’s schema and the reader’s schema side by side and translating
the data from the writer’s schema into the reader’s schema

If the code
reading the data encounters a field that appears in the writer’s schema but not in the reader’s
schema, it is ignored. If the code reading the data expects some field, but the writer’s schema does
not contain a field of that name, it is filled in with a default value declared in the reader’s
schema

With Avro, forward compatibility means that you can have a new version of the schema as writer and
an old version of the schema as reader. Conversely, backward compatibility means that you can have a
new version of the schema as reader and an old version as writer.

Consequently, Avro doesn’t have optional and required markers

The simplest
solution is to include a version number at the beginning of every encoded record, and to keep a
list of schema versions in your database

When two processes are communicating over a bidirectional network connection, they can negotiate
the schema version on connection setup and then use that schema for the lifetime of the
connection

Now, if the database schema changes (for example, a table has one column added and one column
removed), you can just generate a new Avro schema from the updated database schema and export data in
the new Avro schema. The data export process does not need to pay any attention to the schema
change

By contrast, if you were using Thrift or Protocol Buffers for this purpose, the field tags would
likely have to be assigned by hand: every time the database schema changes, an administrator would
have to manually update the mapping from database column names to field tags. 

In dynamically typed programming languages such as JavaScript, Ruby, or Python, there is not much
point in generating code, since there is no compile-time type checker to satisfy. Code generation is
often frowned upon in these languages, since they otherwise avoid an explicit compilation step

if you decode a database value into model objects in the application

and later reencode
those model objects, the unknown field might be lost in that translation process. Solving this is
not a hard problem; you just need to be aware of it.




The web works this way: clients (web browsers) make requests to web servers, making GET requests
to download HTML, CSS, JavaScript, images, etc., and making POST requests to submit data to the
server. The API consists of a standardized set of protocols and data formats (HTTP, URLs, SSL/TLS,
HTML, etc.). Because web browsers, web servers, and website authors mostly agree on these standards,
you can use any web browser to access any website

A key design goal of a service-oriented/microservices architecture is to make the application easier
to change and maintain by making services independently deployable and evolvable

REST is not a protocol, but rather a design philosophy that builds upon the principles of HTTP


SOAP is an XML-based protocol for making network API
requests

The API of a SOAP web service is described using an XML-based language called the Web Services
Description Language, or WSDL

WSDL enables code generation so that a client can access a remote
service using local classes and method calls

users of SOAP rely heavily on tool support, code generation, and IDEs


RESTful APIs tend to favor simpler approaches, typically involving less code generation and
automated tooling

The RPC model tries to make a request to a remote network service look the same as calling a function or
method in your programming language, within the same process (this abstraction is called location
transparency

network request is unpredictable: the request or response may be
lost due to a network problem, or the remote machine may be slow or unavailable, and such problems
are entirely outside of your control

A network request has another possible
outcome: it may return without a result, due to a timeout

A network
request is much slower than a function call

When you call a local function, you can efficiently pass it references (pointers) to objects in
local memory. When you make a network request, all those parameters need to be encoded into a
sequence of bytes that can be sent over the network

The client and the service may be implemented in different programming languages, so the RPC
framework must translate datatypes from one language into another

Custom RPC protocols with a binary encoding format can achieve better performance than something
generic like JSON over REST

The main focus of RPC
frameworks is on requests between services owned by the same organization, typically within the same
datacenter.

For RESTful APIs, common approaches are to use a version
number in the URL or in the HTTP Accept header

They are similar to RPC in that a client’s request (usually
called a message) is delivered to another process with low latency. They are similar to databases
in that the message is not sent via a direct network connection, but goes via an intermediary called
a message broker

It can act as a buffer if the recipient is unavailable or overloaded

It can automatically redeliver messages to a process that has crashed, and thus prevent messages from
being lost.

It avoids the sender needing to know the IP address and port number of the recipient

It allows one message to be sent to several recipients.

It logically decouples the sender from the recipient 

the sender doesn’t wait for the message to be delivered, but simply sends it and
then forgets about it

one process sends a message to a named queue or topic, and the
broker ensures that the message is delivered to one or more consumers of or subscribers to that
queue or topic. There can be many producers and many consumers on the same topic.

Programming language–specific encodings are restricted to a single programming language and often
fail to provide forward and backward compatibility.

These formats are somewhat vague about datatypes, so you have to be careful with things
like numbers and binary strings.

efficient
encoding with clearly defined forward and backward compatibility semantics

However, they have the
downside that data needs to be decoded before it is human-readable.

Databases, where the process writing to the database encodes the data and the process reading
from the database decodes it

RPC and REST APIs, where the client encodes a request, the server decodes the request and encodes
a response, and the client finally decodes the response

Asynchronous message passing (using message brokers or actors), where nodes communicate by sending
each other messages that are encoded by the sender and decoded by the recipient

The problem with a shared-memory approach is that the cost grows faster than linearly

Another approach is the shared-disk architecture, which uses several machines with
independent CPUs and RAM, but stores data on an array of disks that is shared between the machines,
which are connected via a fast network.ii This architecture is used
for some data warehousing workloads, but contention and the overhead of locking limit the
scalability of the shared-disk approach

Keeping a copy of the same data on several different nodes, potentially in different
    locations

Splitting a big database into smaller subsets called partitions so that different
    partitions can be assigned to different nodes (also known as sharding).

Every write to the database needs to be processed by every replica; otherwise, the replicas would no
longer contain the same data. The most common solution for this is called leader-based
replication (also known as active/passive or master–slave replication) and is illustrated

One of the replicas is designated the leader (also known as master or primary). When
clients want to write to the database, they must send their requests to the leader, which first
writes the new data to its local storage.









The other replicas are known as followers

it also sends the
data change to all of its followers as part of a  replication log or
change stream

Each follower takes the log from the leader and updates its local copy of the
database accordingly,

When a client wants to read from the database, it can query either the leader or any of the
followers. However, writes are only accepted on the leader

Synchronous Versus Asynchronous Replication  _NOTE: Asynchronous = eventual consistency, high availability
Synchronous = strong consistency, low availability _

In the example of Figure 5-2, the replication to follower 1 is
synchronous: the leader waits until follower 1 has confirmed that it received the write before
reporting success to the user, and before making the write visible to other clients. The replication
to follower 2 is asynchronous:

The disadvantage is that if the synchronous
follower doesn’t respond (because it has crashed, or there is a network fault, or for any other
reason), the write cannot be processed. The leader must block all writes and wait until the
synchronous replica is available again.

For that reason, it is impractical for all followers to be synchronous: any one node outage would
cause the whole system to grind to a halt

In practice, if you enable synchronous replication on a
database, it usually means that one of the followers is synchronous, and the others are
asynchronous. If the synchronous follower becomes unavailable or slow, one of the asynchronous
followers is made synchronous. This guarantees that you have an up-to-date copy of the data on at
least two nodes: the leader and one synchronous follower. This configuration is sometimes also
called semi-synchronous [7].

Often, leader-based replication is configured to be completely asynchronous. In this case, if the
leader fails and is not recoverable, any writes that have not yet been replicated to followers are
lost. This means that a write is not guaranteed to be durable, even if it has been confirmed to the
client. However, a fully asynchronous configuration has the advantage that the leader can continue
processing writes, even if all of its followers have fallen behind.

Conceptually, the process looks like this:

On its local disk, each follower keeps a log of the data changes it has received from the leader. 

so most systems simply use a timeout: nodes frequently bounce messages back and
forth between each other, and if a node doesn’t respond for some period of time—say, 30
seconds—it is assumed to be dead

The best candidate for leadership is usually the replica with the most
up-to-date data changes from the old leader

Any statement that calls a nondeterministic function, such as NOW() to get the current date
and time or RAND() to get a random number, is likely to generate a different value on each
replica.

they must be executed in exactly the same
order on each replica

In the case of a B-tree (see “B-Trees”), which overwrites individual disk blocks,
every modification is first written to a write-ahead log so that the index can be restored
to a consistent state after a crash.

An alternative is to use different log formats for replication and for the storage engine, which
allows the replication log to be decoupled from the storage engine internals. This kind of
replication log is called a logical log

A logical log format is also easier for external applications to parse. This aspect is useful if you want
to send the contents of a database to an external system

Replication Lag  _NOTE: Only concerned with asynchronous replication._

For workloads that consist of mostly reads and only a small percentage of writes
(a common pattern on the web), there is an attractive option: create many followers, and distribute
the read requests across those followers

if you run the same query on the leader and a follower at the same time, you may get
different results, because not all writes have been reflected in the follower

read-your-writes consistency
[24].
This is a guarantee that if the user reloads the page, they will always see any updates they
submitted themselves.

other users’ updates may not be
visible until some later time. However, it reassures the user that their own input has been saved
correctly.

When reading something that the user may have modified, read it from the leader; otherwise, read it
from a follower  _NOTE: Strong consistency for data that matters to the user, eventual consistency for other data_

You could also monitor the replication lag on followers and
prevent queries on any follower that is more than one minute behind the leader.

The client can remember the timestamp of its most recent write—then the system can ensure that the
replica serving any reads for that user reflects updates at least until that timestamp

Monotonic Reads  _NOTE: Read query from different followers may give different results._

moving backward in time.

monotonic reads
only means that if one user makes several reads in sequence, they will not see time go
backward—i.e., they will not read older data after having previously read newer data.

One way of achieving monotonic reads is to make sure that each user always makes their reads from
the same replica (different users can read from different replicas). For example, the replica can be
chosen based on a hash of the user ID

Consistent Prefix Reads  _NOTE: Different partitions operate at different latency. Some part of data maybe up to date and some part may be out of date._

Preventing this kind of anomaly requires another type of guarantee: consistent prefix reads
[23]. This guarantee says that if a sequence of
writes happens in a certain order, then anyone reading those writes will see them appear in the same
order

This is a particular problem in partitioned (sharded) databases

One solution is to make sure that any writes that are causally related to each other are written to
the same partition—but in some applications that cannot be done efficiently.

Leader-based replication has one major downside: there is only one leader, and all writes must go
through it

In this setup, each leader simultaneously acts as a
follower to the other leaders.

Thus, the inter-datacenter network delay is hidden from
users, which means the perceived performance may be better

A multi-leader configuration with asynchronous replication can
usually tolerate network problems better: a temporary network interruption does not prevent writes
being processed

As multi-leader replication is a somewhat retrofitted feature in many databases, there are often
subtle configuration pitfalls and surprising interactions with other database features. For example,
autoincrementing keys, triggers, and integrity constraints can be problematic. For this reason,
multi-leader replication is often considered dangerous territory that should be avoided if possible  _NOTE: Retrofitted = add on_

For example, consider the calendar apps on your mobile phone, your laptop, and other devices. You
need to be able to see your meetings (make read requests) and enter new meetings (make write
requests) at any time, regardless of whether your device currently has an internet connection. If
you make any changes while you are offline, they need to be synced with a server and your other
devices when the device is next online.


In this case, every device has a local database that acts as a leader (it accepts write requests),
and there is an asynchronous multi-leader replication process (sync) between the replicas of your
calendar on all of your devices. The replication lag may be hours or even days, depending on when
you have internet access available.

Real-time collaborative editing applications allow several people to edit a document
simultaneously

If you want to guarantee that there will be no editing conflicts, the application must obtain a lock
on the document before a user can edit it. If another user wants to edit the same document, they
first have to wait until the first user has committed their changes and released the lock. This
collaboration model is equivalent to single-leader replication with transactions on the leader.

However, for faster collaboration, you may want to make the unit of change very small (e.g., a single
keystroke) and avoid locking. This approach allows multiple users to edit simultaneously, but it also brings
all the challenges of multi-leader replication, including requiring conflict resolution

The biggest problem with multi-leader replication is that write conflicts can occur, which means
that conflict resolution is required

This problem does not occur in a single-leader database

If you want synchronous conflict detection, you might as well just use
single-leader replication.

if the application can ensure
that all writes for a particular record go through the same leader, then conflicts cannot occur.

For example, in an application where a user can edit their own data, you can ensure that requests
from a particular user are always routed to the same datacenter and use the leader in that
datacenter for reading and writing

but from any one user’s point of view the
configuration is essentially single-leader.

In a multi-leader configuration, there is no defined ordering of writes, so it’s not clear what the
final value should be

the database must resolve the conflict in a convergent way, which means that all
replicas must arrive at the same final value when all changes have been replicated.

Although this approach
is popular, it is dangerously prone to data loss
[35].

application may
prompt the user or automatically resolve the conflict, and write the result back to the database.
CouchDB works this way, for example

better because it allows messages to travel
along different paths, avoiding a single point of failure.

Some data storage systems take a different approach, abandoning the concept of a leader and
allowing any replica to directly accept writes from clients

On the other hand, in a leaderless configuration, failover does not exist

read requests are also sent to several nodes in parallel.

The client sees that replica 3 has a stale
value and writes the newer value back to that replica. This approach works well for values that are
frequently read.

background process that constantly looks for differences in
the data between replicas and copies any missing data from one replica to another

does not copy writes in
any particular order

In Dynamo-style databases, the parameters n, w, and r are typically configurable. A common
choice is to make n an odd number (typically 3 or 5) and to set w = r =
(n + 1) / 2 (rounded up

The parameters w and r allow you to adjust the probability of stale values
being read, but it’s wise to not take them as absolute guarantees.

By subtracting a follower’s current position from the leader’s
current position, you can measure the amount of replication lag.  _NOTE: Calculate lag for leader based replication._

These
characteristics make databases with leaderless replication appealing for use cases that require
high availability and low latency, and that can tolerate occasional stale reads.

In this situation, it’s likely that fewer than w or r
reachable nodes remain, so the client can no longer reach a quorum.

Each write from a client
is sent to all replicas, regardless of datacenter, but the client usually only waits for
acknowledgment from a quorum of nodes within its local datacenter so that it is unaffected by
delays and interruptions on the cross-datacenter link

The only safe way of using a database with LWW is to ensure that a key is only written once and
thereafter treated as immutable, thus avoiding any concurrent updates to the same key. For example,
a recommended way of using Cassandra is to use a UUID as the key, thus giving each write operation a
unique key

We also say that B is causally dependent on A.

If one operation happened before another, the later
operation should overwrite the earlier operation, but if the operations are concurrent, we have a
conflict that needs to be resolved

it is not important whether they literally overlap in time. Because of problems with clocks
in distributed systems, it is actually quite difficult to tell whether two things happened
at exactly the same time

but it unfortunately requires that the
clients do some extra work: if several operations happen concurrently, clients have to clean up
afterward by merging the concurrently written values

A simple
approach is to just pick one of the values based on a version number or timestamp (last write wins),
but that implies losing data

With the example of a shopping cart, a reasonable approach to merging siblings is to just take the
union

However, if you want to allow people to also remove things from their carts, and not just add
things, then taking the union of siblings may not yield the right result: if you merge two sibling
carts and an item has been removed in only one of them, then the removed item will reappear in the
union of the siblings

instead, the
system must leave a marker with an appropriate version number to indicate that the item has been
removed when merging siblings.  Such a deletion marker is known as a tombstone

The collection of version numbers from all the replicas is called a version vector

Normally, partitions are defined in such a way that each piece of data (each record, row, or
document) belongs to exactly one partition

The main reason for wanting to partition data is scalability. Different partitions can be placed
on different nodes in a shared-nothing cluster

Partitioning is usually combined with replication so that copies of each partition are stored on
multiple nodes. This means that, even though each record belongs to exactly one partition, it may
still be stored on several different nodes for fault tolerance

Our goal with partitioning is to spread the data and the query load evenly across nodes.

The presence of skew makes partitioning much less effective. In an extreme case, all the load
could end up on one partition, so 9 out of 10 nodes are idle and your bottleneck is the
single busy node. A partition with disproportionately high load is called a hot spot.

Because of this risk of skew and hot spots, many distributed datastores use a hash function to
determine the partition for a given key.

Even if the input strings are very similar, their
hashes are evenly distributed across that range of numbers.

Consistent hashing, as defined by Karger et al.
[7],
is a way of evenly distributing load across an internet-wide system of caches such as a content
delivery network (CDN). It uses randomly chosen partition boundaries to avoid the need for central
control or distributed consensus. Note that consistent here has nothing to do with replica
consistency (see Chapter 5) or ACID consistency (see Chapter 7), but rather
describes a particular approach to rebalancing.

Unfortunately however, by using the hash of the key for partitioning we lose a nice property of
key-range partitioning: the ability to do efficient range queries. Keys that were once adjacent are
now scattered across all the partitions, so their sort order is lost

Cassandra achieves a compromise between the two partitioning strategies
[11,
12,
13].
A table in Cassandra can be declared with a compound primary key consisting of several columns.
Only the first part of that key is hashed to determine the partition, but the other columns are used
as a concatenated index for sorting the data in Cassandra’s SSTables. A query therefore cannot
search for a range of values within the first column of a compound key, but if it specifies a fixed
value for the first column, it can perform an efficient range scan over the other columns of the
key.


The concatenated index approach enables an elegant data model for one-to-many relationships. For
example, on a social media site, one user may post many updates. If the primary key for updates is
chosen to be (user_id, update_timestamp), then you can efficiently retrieve all updates made by a
particular user within some time interval, sorted by timestamp. Different users may be stored on
different partitions, but within each user, the updates are stored ordered by timestamp on a single
partition.  _NOTE: This is what we did for performing range queries on model history.. we store a pair of session id and timestamp as composite key. The timestamp is used for maintaining the sorted order of the conversation and the session id is used for the hash. This allows us to perform efficient range queries since we have a one to many model._

Just a two-digit decimal random number would split the writes to the key evenly across 100 different
keys, allowing those keys to be distributed to different partitions.

However, having split the writes across different keys, any reads now have to do additional work, as
they have to read the data from all 100 keys and combine it

you
also need some way of keeping track of which keys are being split.

A secondary index usually doesn’t identify a record uniquely but
rather is a way of searching for occurrences of a particular value

raison d’être  _NOTE: Reason for existence _

Thus, if you want to search for red cars, you need to
send the query to all partitions, and combine all the results you get back

Most database vendors recommend that you structure
your partitioning scheme so that secondary index queries can be served from a single partition

Rather than each partition having its own secondary index (a local index), we can construct a
global index that covers data in all partitions.

A global
index must also be partitioned, but it can be partitioned differently from the primary key index

We call this kind of index term-partitioned, because the term we’re looking for determines the partition
of the index

The advantage of a global (term-partitioned) index over a document-partitioned index is that it can
make reads more efficient: rather than doing scatter/gather over all partitions, a client only needs
to make a request to the partition containing the term that it wants. However, the downside of a
global index is that writes are slower and more complicated, because a write to a single
document may now affect multiple partitions of the index

The process of
moving load from one node in the cluster to another is called rebalancing

We need an approach that doesn’t move data around more than necessary

Now, if a node is added to the cluster, the new node can steal a few partitions from every
existing node until partitions are fairly distributed once again

If a node is removed from the cluster, the same happens in
reverse.

Only entire partitions are moved between nodes. The number of partitions does not change, nor does
the assignment of keys to partitions

If partitions are very large, rebalancing and recovery from
node failures become expensive. But if partitions are too small, they incur too much overhead. The
best performance is achieved when the size of partitions is “just right,” neither too big nor too
small, which can be hard to achieve if the number of partitions is fixed but the dataset size
varies.

A
transaction is a way for an application to group several reads and writes together into a logical
unit. Conceptually, all the reads and writes in a transaction are executed as one operation: either
the entire transaction succeeds (commit) or it fails (abort, rollback). If it fails, the
application can safely retry

The safety guarantees provided by transactions are often described by the well-known acronym ACID,
which stands for Atomicity, Consistency, Isolation, and Durability

Systems that do not meet the ACID criteria are sometimes called BASE, which stands for
Basically Available, Soft state, and Eventual consistency
[9].
This is even more vague than the definition of ACID. It seems that the only sensible definition of
BASE is “not ACID”; i.e., it can mean almost anything you want.

In general, atomic refers to something that cannot be broken down into smaller parts

ACID atomicity describes what happens if a client wants to make several writes, but a fault
occurs after some of the writes have been processed

database must
discard or undo any writes it has made so far in that transaction.

Isolation in the sense of ACID means that concurrently executing transactions are isolated from
each other: they cannot step on each other’s toes. The classic database textbooks formalize
isolation as serializability, which means that each transaction can pretend that it is the only
transaction running on the entire database.

The purpose of a database system is to provide a safe place where data can be stored without fear of
losing it. Durability is the promise that once a transaction has committed successfully, any data it
has written will not be forgotten, even if there is a hardware fault or the database crashes.



If an error occurs halfway through a sequence of writes, the transaction should be aborted, and
the writes made up to that point should be discarded

all-or-nothing guarantee.

Concurrently running transactions shouldn’t interfere with each other.

you might find this query to be too slow if there are many emails, and decide to store the
number of unread messages in a separate field (a kind of denormalization  _NOTE: By demoralizing, you agree to store redundant data to answer some queries in less time._

Concurrency bugs are hard to find by testing, because such bugs are only triggered when you get
unlucky with the timing. Such timing issues might occur very rarely, and are usually difficult to
reproduce

serializable isolation means that the database
guarantees that transactions have the same effect as if they ran serially (i.e., one at a time,
without any concurrency).

Rather than blindly relying on tools, we need to develop a good understanding of the kinds of
concurrency problems that exist, and how to prevent them. Then we can build applications that are
reliable and correct, using the tools at our disposal.

When reading from the database, you will only see data that has been committed (no dirty
reads).

When writing to the database, you will only overwrite data that has been committed (no dirty
writes).

Imagine a transaction has written some data to the database, but the transaction has not yet committed or aborted.
Can another transaction see that uncommitted data? If yes, that is called a
dirty read

For example, in Figure 7-2, the
user sees the new unread email but not the updated counter. This is a dirty read of the email.
Seeing the database in a partially updated state is confusing to users and may cause other
transactions to take incorrect decisions.

Transactions running at the read
committed isolation level must prevent dirty writes, usually by delaying the second write until the
first write’s transaction has committed or aborted.



Only one transaction can hold the
lock for any given object; if another transaction wants to write to the same object, it must wait
until the first transaction is committed or aborted before it can acquire the lock and continue.
This locking is done automatically by databases in read committed mode (or stronger isolation
levels).

However, the approach of requiring read locks does not work well in practice, because one
long-running write transaction can force many read-only transactions to wait until the long-running
transaction has completed

for every
object that is written, the database remembers both the old committed value and the new value
set by the transaction that currently holds the write lock. While the transaction is ongoing, any
other transactions that read the object are simply given the old value.

The idea is that each transaction reads from a consistent snapshot of
the database—that is, the transaction sees all the data that was committed in the database at the
start of the transaction

Snapshot isolation is a boon for long-running, read-only queries such as backups and analytics. It
is very hard to reason about the meaning of a query if the data on which it operates is changing at
the same time as the query is executing. When a transaction can see a consistent snapshot of the
database, frozen at a particular point in time, it is much easier to understand.

To implement snapshot isolation, databases use a generalization of the mechanism we saw for
preventing dirty reads

If a database only needed to provide read committed isolation, but not snapshot isolation, it would
be sufficient to keep two versions of an object: the committed version and the
overwritten-but-not-yet-committed version. However, storage engines that support snapshot isolation
typically use MVCC for their read committed isolation level as well. A typical approach is that read
committed uses a separate snapshot for each query, while snapshot isolation uses the same snapshot
for an entire transaction

The lost update problem can occur if an application reads some value from the database, modifies it,
and writes back the modified value (a read-modify-write cycle). If two transactions do this
concurrently, one of the modifications can be lost, because the second write does not include the
first modification

Atomic operations are usually implemented by taking an exclusive lock on the object when it is read
so that no other transaction can read it until the update has been applied

Another option is to simply force all atomic operations to be executed on a single thread.

if any other
transaction tries to concurrently read the same object, it is forced to wait until the first
read-modify-write cycle has completed.

An alternative is to allow them to execute in parallel and, if the
transaction manager detects a lost update, abort the transaction and force it to retry
its read-modify-write cycle.

An advantage of this approach is that databases can perform this check efficiently in conjunction
with snapshot isolation

by allowing an update to happen only if the value has not changed since you last
read it

If the current value does not match what you previously read, the update has no effect, and
the read-modify-write cycle must be retried.

a common approach in such replicated
databases is to allow concurrent writes to create several conflicting versions of a value (also
known as siblings), and to use application code or special data structures to resolve and merge
these versions after the fact.

dirty writes and lost updates, two kinds of race conditions that
can occur when different transactions concurrently try to write to the same objects.

Write skew can occur if two
transactions read the same objects, and then update some of those objects

the second-best option in this case is probably
to explicitly lock the rows that the transaction depends on

This effect, where a write in one transaction changes the result of a search query in another
transaction, is called a phantom

Note that the additional table
isn’t used to store information about the booking—it’s

purely a collection of locks which is used
to prevent bookings on the same room and time range from being modified concurrently

This approach is called materializing conflicts, because it takes a phantom and turns it into a
lock conflict on a concrete set of rows that exist in the database

it’s ugly to let a concurrency control
mechanism leak into the application data model. For those reasons, materializing conflicts should be
considered a last resort if no alternative is possible

Serializable isolation is usually regarded as the strongest isolation level. It guarantees that even
though transactions may execute in parallel, the end result is the same as if they had executed one
at a time, serially, without any concurrency

the database prevents all possible race conditions.

to
execute only one transaction at a time, in serial order, on a single thread. By doing so, we completely
sidestep the problem of detecting and preventing conflicts between transactions: the resulting
isolation is by definition serializable.

A new HTTP request starts a new transaction.

systems with single-threaded serial transaction processing don’t allow interactive
multi-statement transactions. Instead, the application must submit the entire transaction code to
the database ahead of time, as a stored procedure

Executing all transactions serially makes concurrency control much simpler, but limits the
transaction throughput of the database to the speed of a single CPU core on a single machine.
Read-only transactions may execute elsewhere, using snapshot isolation, but for applications with
high write throughput, the single-threaded transaction processor can become a serious bottleneck

Several transactions
are allowed to concurrently read the same object as long as nobody is writing to it. But as soon as
anyone wants to write (modify or delete) an object, exclusive access is required:

In 2PL, writers don’t just block other writers; they also block readers and vice
versa

Snapshot isolation has the mantra readers never block writers, and writers never block
readers

it protects against all the race conditions discussed earlier, including lost updates and write skew.

The blocking of readers and writers is implemented by a having a lock on each object in the
database. The lock can either be in shared mode or in exclusive mode. The lock is used as
follows:

This is where the name “two-phase” comes from: the first phase
(while the transaction is executing) is when the locks are acquired, and the second phase (at the
end of the transaction) is when all the locks are released.

Since so many locks are in use, it can happen quite easily that transaction A is stuck waiting for
transaction B to release its lock, and vice versa. This situation is called deadlock. The database
automatically detects deadlocks between transactions and aborts one of them so that the others can
make progress. The aborted transaction needs to be retried by the application.

transaction throughput and response times of queries are significantly worse
under two-phase locking than under weak isolation.

It
may take just one slow transaction, or one transaction that accesses a lot of data and acquires many
locks, to cause the rest of the system to grind to a halt. This instability is problematic when
robust operation is required

phantoms—that is, one transaction
changing the results of another transaction’s search query

most databases with 2PL
actually implement index-range locking (also known as next-key locking), which is a simplified
approximation of predicate locking

 On the one hand, we
have implementations of serializability that don’t perform well (two-phase locking) or don’t scale
well (serial execution). On the other hand, we have weak isolation levels that have good
performance, but are prone to various race conditions (lost updates, write skew, phantoms, etc.

if anything might possibly go wrong (as indicated by a lock held by another
transaction), it’s better to wait until the situation is safe again before doing anything. It is
like mutual exclusion, which is used to protect data structures in multi-threaded programming

Serial execution is, in a sense, pessimistic to the extreme: it is essentially equivalent to each
transaction having an exclusive lock on the entire database (or one partition of the database) for
the duration of the transaction. We compensate for the pessimism by making each transaction very
fast to execute, so it only needs to hold the “lock” for a short time.

By contrast, serializable snapshot isolation is an optimistic concurrency control technique.
Optimistic in this context means that instead of blocking if something potentially dangerous
happens, transactions continue anyway, in the hope that everything will turn out all right

When a
transaction wants to commit, the database checks whether anything bad happened (i.e., whether
isolation was violated); if so, the transaction is aborted and has to be retried. Only transactions
that executed serializably are allowed to commit.

there is enough spare capacity, and if contention between transactions is not too high,
optimistic concurrency control techniques tend to perform better than pessimistic ones

SSI adds an algorithm for detecting serialization conflicts among writes and
determining which transactions to abort

Why not abort transaction 43 immediately when the stale read is detected?
Well, if transaction 43 was a read-only transaction, it wouldn’t need to be aborted, because there
is no risk of write skew

By avoiding unnecessary aborts, SSI preserves snapshot
isolation’s support for long-running reads from a consistent snapshot.

If the database
keeps track of each transaction’s activity in great detail, it can be precise about which
transactions need to abort, but the bookkeeping overhead can become significant. Less detailed
tracking is faster, but may lead to more transactions being aborted than strictly necessary.

read-only queries can run on a consistent
snapshot without requiring any locks, which is very appealing for read-heavy workloads.  _NOTE: Readers don’t block writers_

Dirty reads

One client reads another client’s writes before they have been committed. The read committed
isolation level and stronger levels prevent dirty reads.

Dirty writes

One client overwrites data that another client has written, but not yet committed. Almost all
transaction implementations prevent dirty writes.

Read skew (nonrepeatable reads)




A client sees different parts of the database at different points in time. This issue is most
commonly prevented with snapshot isolation, which allows a transaction to read from a consistent
snapshot at one point in time. It is usually implemented with multi-version concurrency control
(MVCC).

Lost updates

Two clients concurrently perform a read-modify-write cycle. One overwrites the other’s write
without incorporating its changes, so data is lost. Some implementations of snapshot isolation
prevent this anomaly automatically, while others require a manual lock (SELECT FOR UPDATE).

Write skew

A transaction reads something, makes a decision based on the value it saw, and writes the decision
to the database. However, by the time the write is made, the premise of the decision is no longer
true. Only serializable isolation prevents this anomaly.

Phantom reads

A transaction reads objects that match some search condition. Another client makes a write that
affects the results of that search. Snapshot isolation prevents straightforward phantom reads, but
phantoms in the context of write skew require special treatment, such as index-range locks.



Weak isolation levels protect against some of those anomalies but leave you, the application
developer, to handle others manually (e.g., using explicit locking). Only serializable isolation
protects against all of these issues. We discussed three different approaches to implementing
serializable transactions:

Literally executing transactions in a serial order

If you can make each transaction very fast to execute, and the transaction throughput is low
enough to process on a single CPU core, this is a simple and effective option.

Two-phase locking

For decades this has been the standard way of implementing serializability, but many applications
avoid using it because of its performance characteristics.

Serializable snapshot isolation (SSI)

A fairly new algorithm that avoids most of the downsides of the previous approaches. It uses an
optimistic approach, allowing transactions to proceed without blocking. When a transaction wants
to commit, it is checked, and it is aborted if the execution was not serializable.

This nondeterminism and possibility of partial failures is what makes distributed systems hard to
work with  _NOTE: A single system either fails fully or succeeds completely. But at disturbed system can fail partially_

If one node
fails, a common solution is to simply stop the entire cluster workload. After the faulty node is
repaired, the computation is restarted from the last checkpoint
[7,
8].
Thus, a supercomputer is more like a single-node computer than a distributed system

there is no
such thing as perfect reliability

The fault handling must be part of the software design, and
you (as operator of the software) need to know what behavior to expect from the software in the case
of a fault.

Shared-nothing is not the only way of building systems, but it has become the dominant approach for
building internet services, for several reasons: it’s comparatively cheap because it
requires no special hardware, it can make use of commoditized cloud computing services, and it can
achieve high reliability through redundancy across multiple geographically distributed datacenters

The usual way of handling this issue is a timeout: after some time you give up waiting and assume that
the response is not going to arrive

When one part of the network is cut off from the rest due to a network fault, that is sometimes
called a network partition or netsplit

A long timeout means a long wait until a node is declared dead (and during this time, users may have
to wait or see error messages). A short timeout detects faults faster, but carries a higher risk of
incorrectly declaring a node dead when in fact it has only suffered a temporary slowdown

UDP is a good choice in situations where delayed data is worthless

 The retry happens at the human layer instead.
(“Could you repeat that please? The sound just cut out for a moment.”)  _NOTE: lol_