var exec = require('child_process').exec;

/*
 * 	process.argv is an array containing the command line arguments. 
 * 	[0] The first element will be 'node', 
 * 	[1] the second element will be the name of the JavaScript file. 
 * 	[2] The next elements will be any additional command line arguments.
 */

if(process.argv.length<3)
{
	process.stderr.write("Us: node "+process.argv[1]+" arxiu.txt\n");
	process.exit()	
}

var arxiu = process.argv[2]
comanda = "bash parseCorba.sh "+arxiu

console.log(comanda)

var child = exec(comanda,function(error,stdout,stderr) 
{
	if(error) console.log(error);
	process.stderr.write(stderr);
	console.log()
	var array=stdout.split('\n')
	var nums=[]
	array.forEach(function(element)
	{
		if(element!='')
			nums.push(parseFloat(element))
	})
	console.log(nums)
});
