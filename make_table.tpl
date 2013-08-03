%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<table border="1" style="margin-left:auto;margin-right:auto;">
<caption>Open Items</caption>
%for row in rows:
  <tr>
    <td><a href="/edit/{{row['_id']}}">{{row['task']}}</a></td>
    <td>{{row['status']}}</td>
  </tr>
%end
<tr>
    <td colspan=2><a href="/new">Add a new task</a></td>
  </tr>
</table>

